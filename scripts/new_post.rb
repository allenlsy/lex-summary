#!/usr/bin/env ruby

require "date"
require "fileutils"
require "json"

title, language = ARGV

abort "usage: just new-post \"EPISODE TITLE\" LANGUAGE" if title.nil? || language.nil?

title = title.strip
language = language.strip.downcase
slug = title.downcase
            .gsub(/[^\p{Alnum}]+/u, "-")
            .gsub(/\A-+|-+\z/, "")

abort "episode title cannot be empty" if slug.empty?
abort "language must use lowercase letters, numbers, or hyphens" unless language.match?(/\A[a-z][a-z0-9-]*\z/)

post_date = ENV.fetch("POST_DATE", Date.today.iso8601)
posts_dir = ENV.fetch("POSTS_DIR", File.expand_path("../_posts", __dir__))
filename = "#{post_date}-#{slug}-#{language}.md"
path = File.join(posts_dir, filename)

FileUtils.mkdir_p(posts_dir)
ranks = Dir.glob(File.join(posts_dir, "*.md")).filter_map do |existing_path|
  content = File.read(existing_path)
  next unless content.match?(/^article_id:\s*#{Regexp.escape(slug)}\s*$/)

  if content.match?(/^language:\s*#{Regexp.escape(language)}\s*$/)
    abort "a #{language} variant already exists for #{slug}: #{existing_path}"
  end

  content[/^variant_rank:\s*(\d+)\s*$/, 1]&.to_i
end
variant_rank = ranks.max.to_i + 1

File.write(path, <<~MARKDOWN)
  ---
  layout: post
  title: #{JSON.generate(title)}
  date: #{post_date} 09:00:00 +0000
  article_id: #{slug}
  article_title: #{JSON.generate(title)}
  collection_id: practice-notes
  language: #{language}
  variant_rank: #{variant_rank}
  permalink: /articles/#{slug}/#{language}/
  ---

  Write the summary here.
MARKDOWN

puts "Created #{path}"
