// Synthetic hierarchy: five roots, skipped siblings and four levels for UI tests.
function node(id, title, children = []) {
  return { id, slug: `ui-${id}`, title, children, has_notes: false }
}
export const uiHierarchy = [
  node(1, 'First subject', [node(11, 'First unit'), node(12, 'Second unit', [
    node(121, 'First subtopic'), node(122, 'Second subtopic', [node(1221, 'Nested concept')]),
  ])]),
  node(2, 'Second subject', [node(21, 'Another unit')]),
  node(3, 'Third subject with a longer descriptive title', [node(31, 'Third subject unit')]),
  node(4, 'Fourth subject', [node(41, 'Fourth subject unit')]),
  node(5, 'Fifth subject', [node(51, 'Fifth subject unit')]),
]
