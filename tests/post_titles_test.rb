#!/usr/bin/env ruby

require "date"
require "yaml"

posts = Dir[File.expand_path("../_posts/*.md", __dir__)].map do |path|
  source = File.read(path, encoding: "UTF-8")
  front_matter = source.match(/\A---\s*\n(.*?)\n---/m)
  abort "FAIL: missing front matter in #{path}" unless front_matter

  metadata = YAML.safe_load(
    front_matter[1],
    permitted_classes: [Date, Time],
    aliases: true
  )
  [path, metadata]
end

errors = []

expected_names = {
  "94-ilya-sutskever-deep-learning" => "Ilya Sutskever",
  "333-andrej-karpathy-tesla-ai-self-driving-optimus-aliens-and-agi" => "Andrej Karpathy",
  "358-aella-sex-work-onlyfans-porn-escorting-dating-and-human-sexuality" => "Aella",
  "389-benjamin-netanyahu-israel-palestine-power-corruption-hate-and-peace" => "Benjamin Netanyahu",
  "390-yuval-noah-harari-human-nature-intelligence-power-and-conspiracies" => "Yuval Noah Harari",
  "415-serhii-plokhy-history-of-ukraine-russia-soviet-union-kgb-nazis-war" => "Serhii Plokhy",
  "416-yann-lecun-meta-ai-open-source-limits-of-llms-agi-the-future-of-ai" => "Yann LeCun",
  "424-bassem-youssef-israel-palestine-gaza-hamas-middle-east-satire-fame" => "Bassem Youssef",
  "432-kevin-spacey-power-controversy-betrayal-truth-love-in-film-and-life" => "Kevin Spacey",
  "435-andrew-huberman-focus-controversy-politics-and-relationships" => "Andrew Huberman",
  "440-pieter-levels-programming-viral-ai-startups-and-digital-nomad-life" => "Pieter Levels",
  "452-dario-amodei-anthropic-ceo-on-claude-agi-the-future-of-ai-humanity" => "Dario Amodei",
  "458-marc-andreessen-trump-power-tech-ai-immigration-future-of-america" => "Marc Andreessen",
  "464-dave-smith-israel-hamas-ukraine-russia-conspiracies-antisemitism" => "Dave Smith",
  "471-sundar-pichai-ceo-of-google-and-alphabet" => "Sundar Pichai",
  "472-terence-tao-hardest-problems-in-mathematics-physics-the-future-of-ai" => "陶哲轩",
  "475-demis-hassabis-future-of-ai-simulating-reality-physics-and-video-games" => "Demis Hassabis",
  "477-keyu-jin-china-s-economy-tariffs-trade-trump-communism-capitalism" => "金刻羽",
  "481-norman-ohler-hitler-nazis-drugs-ww2-blitzkrieg-lsd-mkultra-cia" => "Norman Ohler",
  "484-dan-houser-gta-red-dead-redemption-rockstar-absurd-future-of-gaming" => "Dan Houser",
  "491-openclaw-the-viral-ai-agent-that-broke-the-internet-peter-steinberger" => "Peter Steinberger",
  "494-jensen-huang-nvidia-the-4-trillion-company-the-ai-revolution" => "黄仁勋",
  "1984-by-george-orwell" => "George Orwell"
}

posts.select { |_, metadata| metadata["language"] == "cn" }.each do |path, metadata|
  unless metadata.fetch("title", "").match?(/\p{Han}/)
    errors << "Chinese post title is not translated: #{File.basename(path)}"
  end

  expected_name = expected_names[metadata["article_id"]]
  if expected_name && !metadata.fetch("title", "").include?(expected_name)
    errors << "Chinese post title does not preserve the expected name #{expected_name}: #{File.basename(path)}"
  end
end

posts.group_by { |_, metadata| metadata["article_id"] }.each do |article_id, variants|
  article_titles = variants.map { |_, metadata| metadata["article_title"] }.uniq
  if article_titles.size != 1
    errors << "Variants do not share article_title for #{article_id}"
  end
end

abort "FAIL: #{errors.join("; ")}" unless errors.empty?

puts "PASS: Chinese posts use translated titles"
puts "PASS: variants retain one shared article title"
