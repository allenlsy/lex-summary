#!/usr/bin/env ruby

require "json"

site_dir = ARGV.fetch(0)

def page(site_dir, relative_path)
  File.read(File.join(site_dir, relative_path), encoding: "UTF-8")
end

def assert_includes(source, expected, message)
  abort "FAIL: #{message}" unless source.include?(expected)
end

def json_ld(source)
  source.scan(%r{<script type="application/ld\+json">\s*(.*?)\s*</script>}m).map do |match|
    JSON.parse(match.first)
  end
end

home = page(site_dir, "index.html")
english_article = page(site_dir, "articles/94-ilya-sutskever-deep-learning/en/index.html")
chinese_article = page(site_dir, "articles/94-ilya-sutskever-deep-learning/cn/index.html")
ryan_article = page(site_dir, "articles/ryan-greenblatt/en/index.html")
dan_carlin_article = page(site_dir, "articles/dan-carlin-s-hardcore-history-62-supernova-in-the-east-1/en/index.html")
search = page(site_dir, "search/index.html")
sitemap = page(site_dir, "sitemap.xml")
robots = page(site_dir, "robots.txt")

site_description = "Concise summaries of long-form interviews across the Lex Fridman Podcast, Dwarkesh, Huberman, Joe Rogan, and Dan Carlin, with more podcasters to come."

assert_includes(home, "<title>Long-Form Podcast Summaries · Lex TL;DR</title>", "homepage title is not descriptive")
assert_includes(home, %(<meta name="description" content="#{site_description}">), "homepage description is not targeted")
assert_includes(home, %(<link rel="canonical" href="https://lextldr.com/">), "homepage canonical URL is missing")
assert_includes(home, %(<meta property="og:type" content="website">), "homepage Open Graph type is missing")
assert_includes(home, %(<meta property="og:site_name" content="Lex TL;DR">), "Open Graph site name is missing")
assert_includes(home, %(<meta name="twitter:card" content="summary">), "Twitter card metadata is missing")

home_schema = json_ld(home).find { |entry| entry["@type"] == "WebSite" }
abort "FAIL: homepage WebSite structured data is missing" unless home_schema
abort "FAIL: homepage schema URL is incorrect" unless home_schema["url"] == "https://lextldr.com/"
abort "FAIL: homepage schema does not identify Lex Fridman focus" unless home_schema["description"].include?("Lex Fridman Podcast")

assert_includes(english_article, %(<html lang="en">), "English article language is incorrect")
assert_includes(chinese_article, %(<html lang="zh-CN">), "Chinese article language is not a valid BCP 47 tag")
assert_includes(english_article, %(<link rel="canonical" href="https://lextldr.com/articles/94-ilya-sutskever-deep-learning/en/">), "article canonical URL is missing")
assert_includes(english_article, %(hreflang="en" href="https://lextldr.com/articles/94-ilya-sutskever-deep-learning/en/"), "English hreflang is missing")
assert_includes(english_article, %(hreflang="zh-CN" href="https://lextldr.com/articles/94-ilya-sutskever-deep-learning/cn/"), "Chinese hreflang is missing")
assert_includes(english_article, %(hreflang="x-default" href="https://lextldr.com/articles/94-ilya-sutskever-deep-learning/en/"), "default-language alternate is missing")
assert_includes(english_article, %(<meta property="og:type" content="article">), "article Open Graph type is missing")
assert_includes(ryan_article, %(href="https://www.dwarkesh.com/p/ryan-greenblatt"), "Ryan Greenblatt source link is missing")
assert_includes(dan_carlin_article, %(href="https://www.dancarlin.com/product/hardcore-history-62-supernova-in-the-east-i/"), "Dan Carlin source link is missing")

article_schema = json_ld(chinese_article).find { |entry| entry["@type"] == "BlogPosting" }
abort "FAIL: article structured data is missing" unless article_schema
abort "FAIL: article schema headline is not localized" unless article_schema["headline"] == "94 - Ilya Sutskever：深度学习"
abort "FAIL: article schema language is incorrect" unless article_schema["inLanguage"] == "zh-CN"
abort "FAIL: article schema does not identify the source episode" unless article_schema.dig("about", "@type") == "PodcastEpisode"

ryan_schema = json_ld(ryan_article).find { |entry| entry["@type"] == "BlogPosting" }
abort "FAIL: Ryan Greenblatt structured data is missing" unless ryan_schema
abort "FAIL: Ryan Greenblatt source URL is missing from structured data" unless ryan_schema.dig("about", "url") == "https://www.dwarkesh.com/p/ryan-greenblatt"

dan_carlin_schema = json_ld(dan_carlin_article).find { |entry| entry["@type"] == "BlogPosting" }
abort "FAIL: Dan Carlin structured data is missing" unless dan_carlin_schema
abort "FAIL: Dan Carlin source URL is missing from structured data" unless dan_carlin_schema.dig("about", "url") == "https://www.dancarlin.com/product/hardcore-history-62-supernova-in-the-east-i/"

assert_includes(search, %(<meta name="robots" content="noindex,follow">), "search page is not marked noindex")
assert_includes(sitemap, "https://lextldr.com/articles/94-ilya-sutskever-deep-learning/en/", "sitemap omits English article")
assert_includes(sitemap, "https://lextldr.com/articles/94-ilya-sutskever-deep-learning/cn/", "sitemap omits Chinese article")
abort "FAIL: sitemap includes the noindex search page" if sitemap.include?("https://lextldr.com/search/")
assert_includes(robots, "Sitemap: https://lextldr.com/sitemap.xml", "robots.txt does not advertise the sitemap")

puts "PASS: rendered pages provide canonical multilingual SEO metadata"
puts "PASS: rendered pages provide source links and structured episode metadata"
puts "PASS: sitemap and robots metadata expose indexable routes"
