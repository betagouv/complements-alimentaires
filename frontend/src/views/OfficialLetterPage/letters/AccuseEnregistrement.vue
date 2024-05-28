<template>
  <OfficialLetterWrapper :letterDate="letterGenerationDate" :letterTitle="title">
    <p>Madame, Monsieur</p>
    <p class="mt-8">
      Le {{ isoToPrettyDate(declarationDate, dateOptions) }}, vous avez déclaré par voie électronique le produit suivant
      :
    </p>
    <div class="my-4 font-bold text-center mx-auto">
      <div>{{ caName }}</div>
      <div>{{ caGalenicForm }}</div>
      <div>{{ caCompany }}</div>
    </div>
    <p>
      Cette déclaration a été effectuée au titre de l’article 15 du décret n°2006-352 du 20 mars 2006 relatif aux
      compléments alimentaires, pour le compte de la société
      <span class="uppercase">{{ caCompany }}.</span>
    </p>
    <p class="font-bold">Votre dossier porte le numéro : {{ caseNumber }}</p>
    <p>Ce numéro unique facilitera le suivi de votre dossier.</p>
    <p>
      Nous vous rappelons qu’il est de votre responsabilité de déclarer et mettre en marché un produit conforme à la
      réglementation applicable aux denrées alimentaires (notamment les règlements (CE) n°178/2002, (UE) n°1169/ 2011 et
      n°2283/2015).
    </p>
    <p>
      A cet effet, vous voudrez bien transmettre, par mail à l’adresse
      <a :href="`mailto:${transmissionEmail}`">{{ transmissionEmail }}</a>
      l’engagement ci-après, merci d’indiquer en objet "[n°{{ caseNumber }}– Engagement]". Ce document peut également
      être téléchargé depuis le site de la DGAL à l’adresse suivante :
      <a :href="dgalDocumentUrl">{{ dgalDocumentUrl }}.</a>
      Votre dossier est susceptible de faire l’objet d’un examen par nos services.
    </p>
    <p>
      Sauf incomplétude du dossier de déclaration, examen défavorable par nos services, ou contrordre de votre part,
      votre produit fera l’objet, sous deux mois, d’une attestation de déclaration et d’une inscription à la liste des
      compléments alimentaires consultable à l’adresse suivante :
      <a :href="attestationUrl">{{ attestationUrl }}</a>
      .
    </p>
    <p>
      Pour tout renseignement d’ordre général sur le cadre réglementaire applicable aux compléments alimentaires, nous
      vous invitons à vous rendre sur le site de la DGAL à l’adresse suivante :
      <a :href="moreLegalInfoUrl">{{ moreLegalInfoUrl }}</a>
      .
    </p>

    <!-- PAGE ENGAGEMENT DE CONFORMITE -->
    <div class="print-break mb-6 text-base font-bold text-center border border-black p-1">
      Compléments alimentaires - Engagement de conformité au droit alimentaire
    </div>
    <p>
      En lien avec la déclaration effectuée au titre de l’article 15 du décret n°2006-352 du 20 mars 2006 relatif aux
      compléments alimentaires,
    </p>
    <p>
      la société
      <span class="uppercase font-bold">{{ caCompany }}</span>
    </p>
    <p>atteste que le produit qu’elle met sur le marché</p>
    <div class="my-4 font-bold">
      <div>{{ caName }}</div>
      <div>{{ caGalenicForm }}</div>
      <div>{{ caCompany }},</div>
    </div>
    <p>
      enregistré sous le numéro
      <span class="font-bold">{{ caseNumber }}</span>
    </p>
    <p>
      répond aux prescriptions du droit alimentaire qui lui sont applicables, notamment les textes précisés en annexe 1
      du présent engagement (liste non exhaustive).
    </p>
    <div class="flex justify-end font-bold">
      <div class="text-left">
        <div>Le {{ isoToPrettyDate(letterGenerationDate, dateOptions) }}</div>
        <div class="uppercase">{{ caCompany }}</div>
        <div>Signature</div>
      </div>
    </div>

    <!-- PAGE ANNEXE 1 -->
    <div class="print-break mb-6 text-base font-bold text-center border border-black p-1">
      Annexe 1 : prescriptions du droit alimentaire applicables aux compléments alimentaires (liste non exhaustive)
    </div>
    <ul>
      <li v-for="law in laws" :key="law.title">
        <a :href="law.url">{{ law.title }}</a>
        {{ law.description }}
      </li>
    </ul>
  </OfficialLetterWrapper>
</template>

<script setup>
import OfficialLetterWrapper from "../OfficialLetterWrapper"
import { isoToPrettyDate } from "@/utils/date"

const laws = [
  {
    title: "Directive n°2002/46/CE",
    url: "https://eur-lex.europa.eu/legal-content/FR/TXT/PDF/?uri=CELEX:02002L0046-20220930&from=EN",
    description:
      "du Parlement européen et du Conseil du 10 juin 2002 relative au rapprochement des législations des Etats membres concernant les compléments alimentaires et le décret n°2006-352 du 20 mars 2006 relatif aux compléments alimentaires",
  },
  {
    title: "Règlement (CE) n°178/2002",
    url: "http://eur-lex.europa.eu/legal-content/FR/ALL/?uri=CELEX%3A32002R0178",
    description:
      "du Parlement européen et du Conseil du 28 janvier 2002 établissant les principes généraux et les prescriptions générales de la législation alimentaire, instituant l'Autorité européenne de sécurité des aliments et fixant des procédures relatives à la sécurité des denrées alimentaires",
  },
  {
    title: "Règlement (CE) n°852/2004",
    url: "https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=celex%3A32004R0852",
    description: "du parlement européen et du Conseil du 29 avril 2004 relatif à l'hygiène des denrées alimentaires",
  },
  {
    title: "Règlement (CE) n°1881/2006",
    url: "https://eur-lex.europa.eu/legal-content/fr/ALL/?uri=CELEX%3A32006R1881",
    description:
      "de la Commission du 19 décembre 2006 portant fixation de teneurs maximales pour certains contaminants dans les denrées alimentaires",
  },
  {
    title: "Règlement (CE) n°1924/2006",
    url: "http://eur-lex.europa.eu/legal-content/FR/TXT/?uri=celex:32006R1924",
    description:
      "du Parlement européen et du Conseil du 20 décembre 2006 concernant les allégations nutritionnelles et de santé portant sur les denrées alimentaires",
  },
  {
    title: "Règlement (CE) n°1925/2006",
    url: "https://eur-lex.europa.eu/legal-content/FR/ALL/?uri=celex:32006R1925",
    description:
      "du Parlement européen et du Conseil du 20 décembre 2006 concernant l'adjonction de vitamines, de minéraux et de certaines autres substances aux denrées alimentaires",
  },
  {
    title: "Règlement (CE) n°1333/2008",
    url: "https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=celex%3A32008R1333",
    description: "du Parlement européen et du Conseil du 16 décembre 2008 sur les additifs alimentaires",
  },
  {
    title: "Règlement (CE) n°1334/2008",
    url: "https://eur-lex.europa.eu/legal-content/FR/ALL/?uri=CELEX%3A32008R1334",
    description:
      "du Parlement européen et du Conseil du 16 décembre 2008 relatif aux arômes et à certains ingrédients alimentaires possédant des propriétés aromatisantes qui sont destinés à être utilisés dans et sur les denrées alimentaires et modifiant le règlement (CEE) n°1601/91 du Conseil, les règlements (CE) n°2232/96 et (CE) n°110/2008 et la directive 2000/13/CE",
  },
  {
    title: "Règlement (UE) n°1169/2011",
    url: "http://eur-lex.europa.eu/legal-content/fr/ALL/?uri=CELEX:32011R1169",
    description:
      "du Parlement européen et du Conseil du 25 octobre 2011 concernant l’information des consommateurs sur les denrées alimentaires, modifiant les règlements (CE) n°1924/ 2006 et (CE) n°1925/2006 du Parlement européen et du Conseil et abrogeant la directive 87/250/CEE de la Commission, la directive 90/496/CEE du Conseil, la directive 1999/10/CE de la Commission, la directive 2000/13/CE du Parlement européen et du Conseil, les directives 2002/67/CE et 2008/5/CE de la Commission et le règlement (CE) n°608/2004 de la Commission",
  },
  {
    title: "Règlement (UE) n°2015/2283",
    url: "https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=OJ%3AJOL_2015_327_r_0001",
    description:
      "du Parlement européen et du Conseil du 25 novembre 2015 relatif aux nouveaux aliments, modifiant le règlement (UE) n°1169/2011 du Parlement européen et du Conseil et abrogeant le règlement (CE) n°258/97 du Parlement européen et du Conseil et le règlement (CE) n°1852/2001 de la Commission",
  },
]

const dateOptions = {
  month: "short",
  day: "numeric",
  year: "numeric",
}

// props
const title = "accusé d’enregistrement de déclaration d’un complément alimentaire"
const letterGenerationDate = new Date(2024, 5, 25)
const declarationDate = new Date(2024, 5, 25)
const caName = "L-Glutamine 2000"
const caGalenicForm = "Gélule"
const caCompany = "Nutrition Sportive Way"
const caseNumber = "2024-5-1273"
const transmissionEmail = "complement-alimentaire.dgal@agriculture.gouv.fr"
const dgalDocumentUrl = "https://agriculture.gouv.fr/quest-ce-quun-complement-alimentaire"
const attestationUrl = "https://url-a-definir" // TODO
const moreLegalInfoUrl = "https://agriculture.gouv.fr/quest-ce-quun-complement-alimentaire"
</script>

<style scoped>
p {
  @apply letter-p;
}

a {
  @apply letter-a;
}
</style>
