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

article_schema = json_ld(chinese_article).find { |entry| entry["@type"] == "BlogPosting" }
abort "FAIL: article structured data is missing" unless article_schema
abort "FAIL: article schema headline is not localized" unless article_schema["headline"] == "94 - Ilya Sutskever：深度学习"
abort "FAIL: article schema language is incorrect" unless article_schema["inLanguage"] == "zh-CN"
abort "FAIL: article schema does not identify the source episode" unless article_schema.dig("about", "@type") == "PodcastEpisode"

assert_includes(search, %(<meta name="robots" content="noindex,follow">), "search page is not marked noindex")
assert_includes(sitemap, "https://lextldr.com/articles/94-ilya-sutskever-deep-learning/en/", "sitemap omits English article")
assert_includes(sitemap, "https://lextldr.com/articles/94-ilya-sutskever-deep-learning/cn/", "sitemap omits Chinese article")
abort "FAIL: sitemap includes the noindex search page" if sitemap.include?("https://lextldr.com/search/")
assert_includes(robots, "Sitemap: https://lextldr.com/sitemap.xml", "robots.txt does not advertise the sitemap")

puts "PASS: rendered pages provide canonical multilingual SEO metadata"
puts "PASS: rendered pages provide WebSite and BlogPosting structured data"
puts "PASS: sitemap and robots metadata expose indexable routes"
