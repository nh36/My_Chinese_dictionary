local function inline_latex(inlines)
  local doc = pandoc.Pandoc({pandoc.Plain(inlines)})
  local latex = pandoc.write(doc, 'latex')
  latex = latex:gsub('^%s+', ''):gsub('%s+$', '')
  latex = latex:gsub('\\par%s*$', '')
  return latex
end

function Header(el)
  local title = inline_latex(el.content)
  if el.level == 1 then
    return pandoc.RawBlock('latex', '\\section*{' .. title .. '}')
  elseif el.level == 2 then
    return pandoc.RawBlock('latex', '\\subsection*{' .. title .. '}')
  elseif el.level == 3 then
    return pandoc.RawBlock('latex', '\\subsubsection*{' .. title .. '}')
  elseif el.level == 4 then
    return pandoc.RawBlock('latex', '\\paragraph*{' .. title .. '}')
  else
    return pandoc.RawBlock('latex', '\\subparagraph*{' .. title .. '}')
  end
end
