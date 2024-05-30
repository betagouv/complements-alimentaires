<template>
  <OfficialLetterWrapper
    :letterDate="letterGenerationDate"
    :recipientName="recipientName"
    :recipientAddress="recipientAddress"
  >
    <p class="!text-base font-bold">Réf. n°{{ caseNumber }}</p>
    <p>Madame, Monsieur,</p>
    <p>Le {{ isoToPrettyDate(declarationDate, dateOptions) }}, vous avez déclaré la mise sur le marché du produit :</p>
    <p class="!text-center !text-base font-bold">{{ caName }} ({{ caCompany }}) / {{ caGalenicForm }}</p>
    <p class="bg-yellow-200">TODO: historique des échanges à mettre ici</p>
    <p>
      Votre déclaration est donc refusée. En application de l’article 20 du décret n°2006-352 du décret du 20 mars 2006,
      il vous est interdit d’importer pour la mise en libre pratique, de détenir en vue de la vente ou de la
      distribution à titre gratuit, de mettre en vente, de vendre ou de distribuer à titre gratuit le complément
      alimentaire cité ci-dessus.
    </p>
    <p>
      Si vous voulez contester la présente décision, vous avez la possibilité de former, dans un délai de deux mois à
      compter de la présente qui vaut notification, un recours gracieux auprès de mes services. Ce recours est effectué
      par écrit. Vous devez motiver votre recours (expliquer les raisons de droit et les faits qui vous conduisent à
      contester la décision) et joindre la présente déclaration de refus ainsi que tous les documents que vous jugerez
      utiles pour faire réviser la décision. L'absence de décision expresse dans un délai de deux mois vaut rejet de
      votre demande de recours gracieux.
    </p>
    <p>
      En application de l’article 19 du décret n°2006-352 du 20 mars 2006, vous pouvez aussi contester la légalité de la
      présente décision devant le tribunal administratif. Ce recours peut être déposé par un écrit ou en ligne via le
      service Télérecours citoyens
      <a :href="telerecoursUrl">{{ telerecoursUrl }}</a>
      . Comme pour le recours gracieux, vous devez motiver votre requête et joindre la présente déclaration de refus. Ce
      recours juridictionnel devra être enregistré au greffe de la juridiction compétente au plus tard avant
      l’expiration du deuxième mois suivant la date de notification de la présente décision. Dans l’hypothèse où vous
      auriez formé un recours gracieux, la saisine de la juridiction devra intervenir avant un délai de deux mois à
      compter du rejet de ce premier recours.
    </p>
    <p>
      Le recours, qu’il soit gracieux ou juridictionnel, n’est pas suspensif et ne vous permet pas de mettre sur le
      marché le complément alimentaire concerné.
      <br />
      Je vous prie d’agréer, Madame, Monsieur, l’expression de ma considération distinguée.
    </p>
    <div class="flex justify-end">
      <div class="text-left mr-10">
        <p>Le Sous-Directeur de la sécurité sanitaire des aliments</p>
        <p>Éric DUMOULIN</p>
      </div>
    </div>
  </OfficialLetterWrapper>
</template>

<script setup>
import OfficialLetterWrapper from "../OfficialLetterWrapper"
import { isoToPrettyDate } from "@/utils/date"

const dateOptions = {
  month: "short",
  day: "numeric",
  year: "numeric",
}

defineProps({
  recipientName: { type: String, required: true },
  recipientAddress: { type: String, required: true },
  letterGenerationDate: { type: String, required: true },
  caName: { type: String, required: true },
  caGalenicForm: { type: String, required: true },
  caCompany: { type: String, required: true },
  declarationDate: { type: String, required: true },
  caseNumber: { type: String, required: true },
  telerecoursUrl: { type: String, required: true },
})
</script>

<style scoped>
p {
  @apply letter-p;
}

a {
  @apply letter-a;
}
</style>
