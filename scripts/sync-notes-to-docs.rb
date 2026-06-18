#!/usr/bin/env ruby
# frozen_string_literal: true

require "fileutils"
require "pathname"

ROOT = Pathname.new(__dir__).parent.expand_path
DOCS = ROOT / "docs"
NOTES = DOCS / "notes"

SUBJECTS = {
  "computer-networking" => {
    title: "计算机网络",
    source: ROOT / "subjects/computer-networking",
    exclude: [
      %r{\A\.claude/},
      %r{\AAGENTS\.md\z},
      %r{\Aalice\.txt\z}
    ]
  },
  "operating-system" => {
    title: "操作系统",
    source: ROOT / "subjects/operating-system",
    exclude: []
  },
  "cryptography" => {
    title: "密码学引论",
    source: ROOT / "subjects/cryptography",
    exclude: [
      %r{\AUsers/},
      %r{\Aexperiment/third_experiment/a2a_secure_flight_agent/},
      %r{\Aexperiment/third_experiment/report/}
    ]
  },
  "computer-systems" => {
    title: "计算机系统原理",
    source: ROOT / "subjects/computer-systems",
    exclude: []
  }
}.freeze

def markdown_files(base, excludes)
  Dir.glob(base.join("**/*.md")).sort.map do |path|
    rel = Pathname.new(path).relative_path_from(base).to_s
    next if excludes.any? { |pattern| rel.match?(pattern) }
    next if rel == "index.md"
    next if rel == "README.md"

    rel
  end.compact
end

def strip_frontmatter(text)
  return text unless text.start_with?("---\n")

  lines = text.lines
  close = lines[1..]&.find_index { |line| line == "---\n" || line == "---\r\n" }
  return text unless close

  lines[(close + 2)..]&.join || ""
end

def title_for(rel, text)
  if text =~ /^#\s+(.+)$/
    Regexp.last_match(1).strip
  else
    File.basename(rel, ".md")
  end
end

def safe_dest(rel)
  rel
end

def convert_obsidian_links(text, name_map, current_dir)
  converted = text.gsub(/\[\[([^\]|#]+)(#[^\]|]+)?(?:\|([^\]]+))?\]\]/) do
    target = Regexp.last_match(1).strip
    anchor = Regexp.last_match(2).to_s
    label = Regexp.last_match(3) || target
    dest = name_map[target]

    if dest
      rel = Pathname.new(dest).relative_path_from(current_dir).to_s
      "[#{label}](#{rel}#{anchor})"
    else
      label
    end
  end

  converted.gsub(%r{\]\(([^)]+/)?README\.md(#[^)]+)?\)}) do
    prefix = Regexp.last_match(1).to_s
    anchor = Regexp.last_match(2).to_s
    "](#{prefix}index.md#{anchor})"
  end
end

def normalize_math_blocks(text)
  in_fence = false

  text.lines.flat_map do |line|
    stripped = line.strip
    in_fence = !in_fence if stripped.start_with?("```", "~~~")

    if !in_fence && line =~ /\A(\s*(?:>\s*)*)\$\$(.+)\$\$\s*\z/
      prefix = Regexp.last_match(1)
      formula = Regexp.last_match(2).strip
      formula = formula[2..-3].strip if formula.start_with?("\\(") && formula.end_with?("\\)")
      ["#{prefix}$$\n", "#{prefix}#{formula}\n", "#{prefix}$$\n"]
    elsif !in_fence && line =~ /\A(\s*(?:>\s*)*)\$([^$].*[^$])\$\s*\z/
      prefix = Regexp.last_match(1)
      formula = Regexp.last_match(2).strip
      formula = formula[2..-3].strip if formula.start_with?("\\(") && formula.end_with?("\\)")
      ["#{prefix}$$\n", "#{prefix}#{formula}\n", "#{prefix}$$\n"]
    else
      line.gsub(/(?<!\\)\$\$([^$\n]+?)\$\$/) do
        inner = Regexp.last_match(1).strip
        inner = inner[2..-3].strip if inner.start_with?("\\(") && inner.end_with?("\\)")
        "\\(#{inner}\\)"
      end.gsub(/(?<![\\$])\$([^$\n]+?)(?<![\\$])\$(?!\$)/) do
        inner = Regexp.last_match(1).strip
        next "\\(#{inner}\\)" if inner.start_with?("\\(") && inner.end_with?("\\)")

        "\\(#{inner}\\)"
      end
    end
  end.join
end

FileUtils.rm_rf(NOTES)
FileUtils.mkdir_p(NOTES)
File.write(
  NOTES / "index.md",
  [
    "# 课程笔记",
    "",
    "这里是课程仓库 Markdown 笔记的站内 Wiki 版本。笔记会同步到本站页面，可直接阅读、搜索和互相跳转。",
    "",
    "- [计算机网络](computer-networking/index.md)",
    "- [操作系统](operating-system/index.md)",
    "- [密码学引论](cryptography/index.md)",
    "- [计算机系统原理](computer-systems/index.md)",
    ""
  ].join("\n")
)

subject_indexes = {}

SUBJECTS.each do |slug, cfg|
  source = cfg[:source]
  dest_root = NOTES / slug
  files = markdown_files(source, cfg[:exclude])
  name_map = {}

  files.each do |rel|
    dest = dest_root / safe_dest(rel)
    name_map[File.basename(rel, ".md")] = dest.relative_path_from(DOCS).to_s
  end

  entries = []

  files.each do |rel|
    source_file = source / rel
    dest_file = dest_root / safe_dest(rel)
    FileUtils.mkdir_p(dest_file.dirname)

    raw = File.read(source_file)
    body = strip_frontmatter(raw).lstrip
    title = title_for(rel, body)
    current_dir = dest_file.dirname.relative_path_from(DOCS)
    converted = normalize_math_blocks(convert_obsidian_links(body, name_map, current_dir))

    page = +"# #{title}\n\n"
    page << "> 来源：`#{cfg[:title]} / #{rel}`\n\n"
    page << converted.sub(/\A#\s+.+\n+/, "")
    File.write(dest_file, page)

    entries << [rel, title, dest_file.relative_path_from(DOCS).to_s]
  end

  subject_indexes[slug] = entries

  lines = []
  lines << "# #{cfg[:title]}笔记"
  lines << ""
  lines << "这里收录从课程仓库同步来的 Markdown 笔记，可在本站内直接阅读和搜索。"
  lines << ""
  entries.group_by { |entry| File.dirname(entry[0]) == "." ? "入口" : File.dirname(entry[0]) }.each do |group, group_entries|
    lines << "## #{group}"
    lines << ""
    group_entries.each do |_rel, title, dest|
      lines << "- [#{title}](#{Pathname.new(dest).relative_path_from(Pathname.new("notes/#{slug}")).to_s})"
    end
    lines << ""
  end
  File.write(dest_root / "index.md", lines.join("\n"))
end

puts "Synced notes:"
subject_indexes.each do |slug, entries|
  puts "- #{slug}: #{entries.length}"
end
