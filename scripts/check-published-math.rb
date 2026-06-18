#!/usr/bin/env ruby
# frozen_string_literal: true

require "pathname"

ROOT = Pathname.new(__dir__).parent.expand_path
DOCS_NOTES = ROOT / "docs/notes"

offenses = []

Dir.glob(DOCS_NOTES.join("**/*.md")).sort.each do |path|
  File.foreach(path).with_index(1) do |line, number|
    if line.include?("\\[") || line.include?("\\]")
      offenses << "#{Pathname.new(path).relative_path_from(ROOT)}:#{number}: #{line.strip}"
    end
  end
end

if offenses.empty?
  puts "Published math check passed."
else
  warn "Found Markdown-sensitive \\[ or \\] display math delimiters in published notes:"
  warn offenses.join("\n")
  exit 1
end
