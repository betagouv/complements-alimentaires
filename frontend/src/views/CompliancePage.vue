<template>
  <div class="fr-container pb-10">
    <DsfrBreadcrumb :links="[{ to: '/', text: 'Accueil' }, { text: 'Conformité au droit alimentaire' }]" />
    <h1>Conformité au droit alimentaire</h1>

    <DsfrCallout>
      Consultez également l'article
      <a
        href="https://agriculture.gouv.fr/quest-ce-quun-complement-alimentaire"
        target="_blank"
        ref="noopener external"
        title="Qu'est-ce qu'un complément alimentaire ? - nouvelle fenêtre"
      >
        Qu'est-ce qu'un complément alimentaire ?
      </a>
    </DsfrCallout>
    <p>
      Les compléments alimentaires déclarés sur Compl'Alim doivent répondre aux prescriptions du droit alimentaire qui
      lui sont applicables, notamment par rapport aux textes précisés ci-dessous (liste non exhaustive).
    </p>

    <div class="grid grid-cols-12 gap-6">
      <DsfrCard
        class="col-span-12 sm:col-span-6 md:col-span-4"
        v-for="item in items"
        :key="item.title"
        :title="item.title"
        :description="item.body"
        :link="item.link"
      />
    </div>
  </div>
</template>

<script setup>
const items = [
  {
    title: "Directive n°2002/46/CE",
    body: "du Parlement européen et du Conseil du 10 juin 2002 relative au rapprochement des législations des Etats membres concernant les compléments alimentaires.",
    link: "https://eur-lex.europa.eu/legal-content/FR/TXT/PDF/?uri=CELEX",
  },
  {
    title: "Décret n°2006-352",
    body: "du 20 mars 2006 relatif aux compléments alimentaires.",
    link: "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000638341",
  },
  {
    title: "Règlement (CE) n°178/2002",
    body: "du Parlement européen et du Conseil du 28 janvier 2002 établissant les principes généraux et les prescriptions générales de la législation alimentaire, instituant l'Autorité européenne de sécurité des aliments et fixant des procédures relatives à la sécurité des denrées alimentaires.",
    link: "https://eur-lex.europa.eu/legal-content/FR/ALL/?uri=CELEX%3A32002R0178",
  },
  {
    title: "Règlement (CE) n°852/2004",
    body: "du Parlement européen et du Conseil du 29 avril 2004 relatif à l'hygiène des denrées alimentaires.",
    link: "https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=celex%3A32004R0852",
  },
  {
    title: "Règlement (UE) n°2023/915",
    body: "du Règlement (UE) 2023/915 de la Commission du 25 avril 2023 concernant les teneurs maximales pour certains contaminants dans les denrées alimentaires et abrogeant le règlement (CE) no 1881/2006 (Texte présentant de l’intérêt pour l’EEE)",
    link: "https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX%3A32023R0915",
  },
  {
    title: "Règlement (CE) n°1924/2006",
    body: "du Parlement européen et du Conseil du 20 décembre 2006 concernant les allégations nutritionnelles et de santé portant sur les denrées alimentaires.",
    link: "https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=celex:32006R1924",
  },
  {
    title: "Règlement (CE) n°1925/2006",
    body: "du Parlement européen et du Conseil du 20 décembre 2006 concernant l'adjonction de vitamines, de minéraux et de certaines autres substances aux denrées alimentaires.",
    link: "https://eur-lex.europa.eu/legal-content/FR/ALL/?uri=celex:32006R1925",
  },
  {
    title: "Règlement (CE) n°1333/2008",
    body: "du Parlement européen et du Conseil du 16 décembre 2008 sur les additifs alimentaires.",
    link: "https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=celex%3A32008R1333",
  },
  {
    title: "Règlement (CE) n°1334/2008",
    body: "du Parlement européen et du Conseil du 16 décembre 2008 relatif aux arômes et à certains ingrédients alimentaires possédant des propriétés aromatisantes qui sont destinés à être utilisés dans et sur les denrées alimentaires et modifiant le règlement (CEE) n°1601/91 du Conseil, les règlements (CE) n°2232/96 et (CE) n°110/2008 et la directive 2000/13/CE.",
    link: "https://eur-lex.europa.eu/legal-content/FR/ALL/?uri=CELEX%3A32008R1334",
  },
  {
    title: "Règlement (UE) n°1169/2011",
    body: "du Parlement européen et du Conseil du 25 octobre 2011 concernant l’information des consommateurs sur les denrées alimentaires, modifiant les règlements (CE) n°1924/ 2006 et (CE) n°1925/2006 du Parlement européen et du Conseil et abrogeant la directive 87/250/CEE de la Commission, la directive 90/496/CEE du Conseil, la directive 1999/10/CE de la Commission, la directive 2000/13/CE du Parlement européen et du Conseil, les directives 2002/67/CE et 2008/5/CE de la Commission et le règlement (CE) n°608/2004 de la Commission.",
    link: "https://eur-lex.europa.eu/legal-content/fr/ALL/?uri=CELEX:32011R1169",
  },
  {
    title: "Règlement (UE) n°2015/2283",
    body: "du Parlement européen et du Conseil du 25 novembre 2015 relatif aux nouveaux aliments, modifiant le règlement (UE) n°1169/2011 du Parlement européen et du Conseil et abrogeant le règlement (CE) n°258/97 du Parlement européen et du Conseil et le règlement (CE) n°1852/2001 de la Commission.",
    link: "https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=OJ%3AJOL_2015_327_R_0001",
  },
]
</script>
