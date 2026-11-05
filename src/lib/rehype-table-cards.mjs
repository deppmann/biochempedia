/**
 * rehype-table-cards — make every markdown table in lesson content readable on a phone.
 *
 * Chris, 2026-11-05: lesson tables (449 across 203 lessons) looked crowded, worst on phones. This
 * plugin changes no lesson. For each table it:
 *   - wraps it in <div class="table-cards"> so the site CSS can style it (src/styles/global.css);
 *   - copies each column's header text onto that column's cells as data-label, so on a narrow screen
 *     the CSS can lay each row out as a small card with every value labelled by its column;
 *   - marks the first cell of each row as the row's title (class "tc-title"), and turns it into a
 *     row header (<th scope="row">) when the table's top-left header cell is empty, as in a
 *     "| | A | B |" comparison table;
 *   - adds "tc-stack" to the wrapper when the table has five or more columns: those are cards at
 *     every width, because six columns in the reading column make tall, narrow rows.
 * Plain HTML, no JavaScript. A screen reader still gets a real table.
 */

const text = (n) => (n.type === 'text' ? n.value : (n.children || []).map(text).join(''));
const isEl = (n, tag) => n && n.type === 'element' && n.tagName === tag;
const kids = (n, tag) => (n.children || []).filter((c) => isEl(c, tag));

function visit(node, fn, parent = null, index = 0) {
  fn(node, parent, index);
  (node.children || []).forEach((c, i) => visit(c, fn, node, i));
}

export default function rehypeTableCards() {
  return (tree) => {
    const tables = [];
    visit(tree, (node, parent, index) => {
      if (isEl(node, 'table') && parent && !(isEl(parent, 'div') && (parent.properties?.className || []).includes('table-cards')))
        tables.push({ node, parent, index });
    });
    // Wrap from the end so earlier indexes stay valid.
    for (const { node, parent, index } of tables.reverse()) {
      const thead = kids(node, 'thead')[0];
      const headRow = thead ? kids(thead, 'tr')[0] : null;
      const labels = headRow ? (headRow.children || []).filter((c) => isEl(c, 'th') || isEl(c, 'td')).map((c) => text(c).trim()) : [];
      const rowHeads = labels.length > 1 && labels[0] === '';
      for (const body of kids(node, 'tbody')) {
        for (const tr of kids(body, 'tr')) {
          let col = 0;
          for (const cell of tr.children || []) {
            if (!isEl(cell, 'td') && !isEl(cell, 'th')) continue;
            cell.properties = cell.properties || {};
            if (labels[col]) cell.properties.dataLabel = labels[col];
            if (col === 0) {
              cell.properties.className = [...(cell.properties.className || []), 'tc-title'];
              if (rowHeads) { cell.tagName = 'th'; cell.properties.scope = 'row'; }
            }
            col++;
          }
        }
      }
      node.properties = node.properties || {};
      node.properties.dataCols = String(labels.length || 0);
      parent.children[index] = { type: 'element', tagName: 'div', properties: { className: labels.length >= 5 ? ['table-cards', 'tc-stack'] : ['table-cards'] }, children: [node] };
    }
  };
}
