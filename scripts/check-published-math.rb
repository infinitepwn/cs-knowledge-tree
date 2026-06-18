#!/usr/bin/env ruby
# frozen_string_literal: true

require "pathname"

ROOT = Pathname.new(__dir__).parent.expand_path
DOCS_NOTES = ROOT / "docs/notes"

offenses = []

Dir.glob(DOCS_NOTES.join("**/*.md")).sort.each do |path|
  File.foreach(path).with_index(1) do |line, number|
    offenses << "#{Pathname.new(path).relative_path_from(ROOT)}:#{number}: #{line.strip}" if line.include?("$$")
  end
end

if offenses.empty?
  puts "Published math check passed."
else
  warn "Found unstable $$ math delimiters in published notes:"
  warn offenses.join("\n")
  exit 1
end
