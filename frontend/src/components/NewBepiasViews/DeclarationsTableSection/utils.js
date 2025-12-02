// Cette fontion diffère de celle sur utils/components car elle traite les
// status simplifiés présents sur la vue du contrôle.
export const getStatusTagForCell = (status) => {
  const tagData = {
    "Commercialisation possible": { icon: "ri-checkbox-circle-fill", color: "green" },
    "En cours d'instruction": { icon: "ri-information-fill", color: "blue" },
    "Commercialisation refusée": { icon: "ri-close-circle-fill", color: "red" },
    "Retiré du marché": { icon: "ri-stop-circle-fill", color: "blue" },
    "Instruction interrompue": { icon: "ri-close-fill", color: "blue" },
  }
  return {
    component: "DsfrTag",
    label: status,
    class: tagData[status]?.color,
    icon: tagData[status]?.icon,
  }
}
