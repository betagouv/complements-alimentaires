export const setDocumentTitle = (parts) => {
  parts.push("Compl'Alim")
  document.title = parts.join(" - ")
}
