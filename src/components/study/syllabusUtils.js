function alphabetic(index) {
  let label = ''
  for (let n = index + 1; n > 0; n = Math.floor((n - 1) / 26)) {
    label = String.fromCharCode(65 + (n - 1) % 26) + label
  }
  return label
}

// Build from the full API tree, before any filtering. Never change stored titles.
export function indexSyllabus(topics, parentPath = [], index = new Map()) {
  topics.forEach((topic, position) => {
    const path = [...parentPath, position + 1]
    const number = path.length === 1 ? String(path[0])
      : path.length === 2 ? path.join('.') : alphabetic(position)
    index.set(topic.slug, { number, path, hasChildren: Boolean(topic.children?.length) })
    indexSyllabus(topic.children || [], path, index)
  })
  return index
}
