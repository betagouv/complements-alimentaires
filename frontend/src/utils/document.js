// multiPage est un objet avec: number, total, term
export const setDocumentTitle = (parts, multiPage) => {
  if (multiPage && multiPage.total > 1) {
    parts.splice(1, 0, `${multiPage.term} ${multiPage.number} sur ${multiPage.total}`)
  }
  parts.push("Compl'Alim")
  document.title = parts.join(" - ")
}
