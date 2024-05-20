import { statusProps } from "@/utils/mappings"

export const getStatusTagForCell = (status) => ({
  component: "DsfrTag",
  label: statusProps[status].label,
  class: status,
  icon: statusProps[status].icon,
})

export const getPagesForPagination = (count, limit, path) => {
  const totalPages = Math.ceil(count / limit)
  const pages = []
  for (let i = 0; i < totalPages; i++)
    pages.push({
      label: i + 1,
      href: `${path}?page=${i + 1}`,
      title: `Page ${i + 1}`,
    })
  return pages
}
