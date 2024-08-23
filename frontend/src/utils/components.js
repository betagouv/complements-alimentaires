import { statusProps } from "@/utils/mappings"

export const getStatusTagForCell = (status, groupInstruction = false) => {
  const instructionStatuses = ["AWAITING_INSTRUCTION", "ONGOING_INSTRUCTION", "AWAITING_VISA", "ONGOING_VISA"]
  const processedStatus = groupInstruction && instructionStatuses.indexOf(status) > -1 ? "INSTRUCTION" : status
  return {
    component: "DsfrTag",
    label: statusProps[processedStatus].label,
    class: processedStatus,
    icon: statusProps[processedStatus].icon,
  }
}

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
