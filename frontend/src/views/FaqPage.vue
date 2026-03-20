<template>
  <div>
    <div class="pt-10 bg-blue-france-975 relative min-h-[160px]">
      <div class="fr-container">
        <h1 class="mb-2">Foire aux questions</h1>
        <p>Documentation pour vous guider dans la prise en main de Compl'Alim.</p>
      </div>
    </div>
    <div class="fr-container pb-10">
      <DsfrAccordionsGroup v-model="activeAccordion">
        <h2 class="fr-h4">Moteur de recherche ingrédients</h2>
        <DsfrAccordion title="Comment fonctionne le moteur de recherche ?">
          <p>
            Le moteur de recherche "Ingrédients" vous permet de vérifier rapidement les recommandations d'usage et la
            conformité des ingrédients que vous envisagez d’utiliser dans vos produits.
          </p>
          <p>
            En consultant les informations sur les doses autorisées, les usages permis et les restrictions
            réglementaires, vous vous assurez que la composition de vos nouveaux produits respecte les normes en vigueur
            dès la phase de conception.
          </p>
          <p>
            Cela vous aide à anticiper les exigences réglementaires et à sécuriser la mise sur le marché de vos
            produits.
          </p>
        </DsfrAccordion>
        <h2 class="fr-h4">Comptes utilisateurs</h2>
        <DsfrAccordion title="Comment créer mon compte ?">
          <ol>
            <li>Rendez-vous sur le site de Compl’Alim et cliquez sur le bouton "S’enregistrer" (en haut à droite) ;</li>
            <li>Renseignez les informations demandées (nom, prénom, adresse email, identifiant et mot de passe) ;</li>
            <li>Vous recevrez alors un mail de confirmation sur l’adresse email que vous avez indiquée ;</li>
            <li>
              Une fois votre adresse email validée, vous pourrez accéder à Compl’Alim avec l’identifiant et le mot de
              passe que vous aurez précédemment choisis.
            </li>
          </ol>
        </DsfrAccordion>
        <DsfrAccordion title="Comment enregistrer/rejoindre mon entreprise ?">
          <ol>
            <li>Connectez-vous à votre compte sur Compl’Alim.</li>
            <li>Accédez à votre tableau de bord (situé dans le menu à droite).</li>
            <li>Cliquez sur la carte "Nouvelle entreprise" dans la section "Mon compte".</li>
            <li>Renseignez le pays et le numéro SIRET de votre entreprise.</li>
            <li>
              Selon le statut de votre entreprise sur Compl’Alim, deux scénarios sont possibles :
              <ul>
                <li>
                  <strong>Votre entreprise n'est pas encore enregistrée</strong>
                  : Vous serez invité.e à fournir les informations nécessaires à son enregistrement. En tant que premier
                  utilisateur à enregistrer cette entreprise, le
                  <strong>rôle de gestionnaire vous sera attribué par défaut</strong>
                  .
                </li>
                <li>
                  <strong>Votre entreprise est déjà enregistrée</strong>
                  : Vous pourrez demander à y être rattaché.e, soit en tant que déclarant soit en tant que gestionnaire.
                  Une notification sera envoyée au gestionnaire actuel de l'entreprise via un email, l’informant de
                  votre demande d'accès.
                </li>
              </ul>
            </li>
          </ol>
        </DsfrAccordion>
        <DsfrAccordion title="Comment inviter des collaborateurs à rejoindre mon entreprise ou supprimer leurs accès ?">
          <p>
            Seuls les gestionnaires ont le pouvoir de gérer les accès des collaborateurs. Pour ajouter un collaborateur,
            voici la marche à suivre :
          </p>
          <ol>
            <li>Connectez-vous à votre compte Compl’Alim.</li>
            <li>Rendez-vous dans votre tableau de bord (menu à droite).</li>
            <li>
              Cliquez sur la carte "Les collaborateurs de mon entreprise" sous la section "Gestion de l’entreprise X".
            </li>
            <li>Cliquez sur "Ajouter un collaborateur" en haut à droite.</li>
            <li>Sélectionnez le rôle à attribuer à la personne (déclarant ou gestionnaire).</li>
            <li>
              Renseignez son adresse email. La personne recevra un email pour finaliser l'inscription et son
              rattachement à l'entreprise.
            </li>
          </ol>
          <p>
            Depuis cette même page, vous pouvez modifier les droits d’un collaborateur (ex. passer de gestionnaire à
            déclarant) ou révoquer ses accès.
          </p>
        </DsfrAccordion>
        <DsfrAccordion title='Quelles différences entre les rôles de "gestionnaire" et de "déclarant" ?'>
          <p>Le gestionnaire et le déclarant jouent des rôles distincts au sein de la plateforme.</p>
          <p>
            Le gestionnaire est responsable de la gestion des informations de l'entreprise ainsi que des collaborateurs
            qui ont les droits de gestion et/ou de déclaration pour cette entreprise.
          </p>
          <p>
            Le déclarant a uniquement le pouvoir de réaliser des déclarations pour le compte de l'entreprise à laquelle
            il est rattaché.
          </p>
          <p>
            <strong>
              ⚠️ Attention, le gestionnaire n'est pas automatiquement déclarant (vous ne pourrez pas déclarer un nouveau
              produit)
            </strong>
            . Pour cumuler les fonctions de gestion et de déclaration, le gestionnaire doit s'attribuer les deux rôles.
          </p>
        </DsfrAccordion>
        <DsfrAccordion
          title="Comment gérer l'accès et le mandat de déclaration pour une entreprise et une société mandataire ?"
        >
          <p>
            Lors du lancement de la plateforme, il n’était pas possible d’inviter directement une société mandataire. Le
            gestionnaire devait inviter individuellement les consultants ou collaborateurs de la société mandatée pour
            leur permettre de réaliser des déclarations au nom son entreprise.
          </p>
          <p>
            Désormais, tous les comptes associés à une société mandataire auront automatiquement l’autorisation de
            déclarer pour les clients ayant confié un mandat à cette entité.
          </p>
          <p>Pour cela, la carte "Entreprises mandatées" est disponible dans votre tableau de bord.</p>
          <p>Voici les étapes à suivre pour rattacher une entreprise :</p>
          <ol>
            <li>Rendez-vous dans la carte "Entreprises mandatées".</li>
            <li>Ajoutez le numéro de SIRET ou le numéro de TVA intracommunautaire de l’entreprise mandatée.</li>
          </ol>
          <p>
            <span aria-hidden="true">⚠️</span>
            Attention : L’entreprise mandatée doit disposer d’un compte sur la plateforme. Si ce n’est pas le cas, elle
            devra en créer un au préalable.
          </p>
          <p>
            Si vous souhaitez ajuster les rôles des déclarants de votre entreprise, n’hésitez pas à nous contacter à
            l'adresse suivante :
            <a :href="`mailto:${contactEmail}`">
              {{ contactEmail }}
            </a>
          </p>
        </DsfrAccordion>
        <h2 class="fr-h4">Déclarations</h2>
        <DsfrAccordion title="Comment déclarer un nouveau produit ?">
          <ol>
            <li>Connectez-vous à votre compte Compl’Alim.</li>
            <li>Rendez-vous dans votre tableau de bord (menu à droite).</li>
            <li>Cliquez sur la carte "Créez une nouvelle déclaration"</li>
            <li>
              Vous allez alors devoir renseigner les informations sur votre complément alimentaire, qui sont réparties
              en 4 onglets distincts :
              <ul>
                <li>"Produit" pour renseigner les informations relatives au produit (comme détaillé ci-dessous) ;</li>
                <li>"Composition" pour indiquer la composition du complément (comme détaillé ci-dessous) ;</li>
                <li>"PJ" pour transmettre vos pièces jointes, notamment l’étiquetage ;</li>
                <li>
                  "Soumettre" où vous aurez un récapitulatif des informations saisies et la possibilité de laisser un
                  commentaire à destination de l'administration.
                </li>
              </ul>
            </li>
          </ol>
          <p>Les champs obligatoires à remplir sont indiqués par une astérix *.</p>
          <p>
            <span aria-hidden="true">💡</span>
            Vous pouvez naviguer librement entre ces onglets sans avoir à remplir tous les champs d'un onglet avant de
            passer au suivant.
          </p>
        </DsfrAccordion>
        <DsfrAccordion title="Comment enregistrer mon brouillon ?">
          <p>
            Toutes vos informations s’enregistrent automatiquement à chaque changement d'étape, en cliquant sur les
            boutons en bas de page "Revenir à l'onglet " ou "Passer à l'onglet ". Si le dossier n’est pas soumis, il
            sera automatiquement sauvegardé en tant que brouillon.
          </p>
        </DsfrAccordion>
        <DsfrAccordion title='Comment remplir les informations demandées dans l’onglet "Produit" ?'>
          <p>
            L'onglet "Produit" vous permet de renseigner les informations principales relatives à votre complément
            alimentaire, telles que son nom, sa marque, son format, les populations cibles, ainsi que les effets
            recherchés. Plus précisément, vous devez renseigner :
          </p>
          <ul>
            <li>Nom de l'entreprise responsable de mise sur le marché du complément alimentaire</li>
            <li>Nom du complément alimentaire</li>
            <li>Marque</li>
            <li>Gamme</li>
            <li>Arôme</li>
            <li>Description : présentation de votre produit</li>
            <li>
              Forme galénique : forme sous laquelle le complément alimentaire se prend (ex : gélules, comprimés...)
            </li>
            <li>Poids/volume d’une unité de consommation</li>
            <li>Conditionnement : type d'emballage (boîte, sachet, etc.)</li>
            <li>Dose journalière recommandée</li>
            <li>Durabilité minimale/DLUO : durée de vie du produit en mois.</li>
            <li>Mode d’emploi : instructions sur comment consommer le produit</li>
            <li>
              <strong>Mise en garde et avertissement</strong>
              : précautions spécifiques à prendre lors de l’utilisation du produit, en particulier celles concernant les
              populations à risque pour lesquelles la consommation est déconseillée. L’étiquetage du produit devra être
              conforme aux avertissements et précautions déclarés dans cette section.
            </li>
            <li>
              <strong>Population cible</strong>
              : populations pour lesquelles le complément alimentaire est spécifiquement conçu. L'option "population
              générale" indique que le produit est destiné à l'ensemble de la population, y compris les nourrissons et
              les enfants. Si vous sélectionnez cette option, il n'est pas nécessaire de cocher les autres cases.
              <span aria-hidden="true">🚀</span>
              Nous travaillons actuellement à simplifier cette liste et vous tiendrons informés dès que cette mise à
              jour sera effectuée.
            </li>
            <li>
              <strong>Populations à risque</strong>
              : catégories de personnes pour lesquelles la consommation du complément alimentaire peut être
              déconseillée. Les mises en garde et avertissements correspondant à ces populations devront être clairement
              indiqués sur l'étiquetage du produit afin de garantir une utilisation sécurisée.
            </li>
            <li>Objectifs/effets : effets recherchés par le complément alimentaire.</li>
            <li>Adresse sur l’étiquetage : adresse postale qui apparaîtra sur l’étiquette.</li>
          </ul>
          <p>
            Si une définition n'est pas claire, n'hésitez pas à nous contacter pour demander des informations
            complémentaires.
          </p>
        </DsfrAccordion>
        <DsfrAccordion title='Comment remplir les informations demandées dans l’onglet "Composition" ?'>
          <p>
            Cet onglet vous permet de renseigner les ingrédients et les substances actives de votre complément
            alimentaire.
          </p>
          <p>
            <strong>
              La section Ingrédients sert à ajouter les éléments constitutifs du produit, tels que les plantes ou autres
              matières premières.
            </strong>
            Pour ajouter un ingrédient, tapez son nom dans le moteur de recherche puis sélectionnez l’ingrédient
            correspondant dans la liste déroulante qui s’affiche.
          </p>
          <p>
            <span aria-hidden="true">💡</span>
            Dans la section "Ingrédients", vous avez désormais la possibilité de préciser si l’ingrédient ajouté joue un
            rôle actif ou non actif dans le produit, afin d'éviter la création de doublons dans la base de données et de
            mieux structurer les informations déclarées.
          </p>
          <p>
            <strong>
              La section "Substances" affiche automatiquement les composés actifs présents dans les ingrédients actifs
            </strong>
            . Une vigilance particulière est accordée à certaines de ces substances, notamment sur la quantité présente
            qui peut conduire à des restrictions d’usage. Il est donc essentiel de les identifier clairement et de
            préciser leurs quantités pour assurer la sécurité et la conformité réglementaire du complément alimentaire.
          </p>
          <p>
            Dans la section "Substances", contrairement à l'ancien outil de déclaration Teleicare, il vous est pour le
            moment demandé de renseigner les quantités présentes dans le produit pour toutes les substances identifiées.
            Cependant, dans les prochains mois, nous allons distinguer les substances pour lesquelles il est obligatoire
            de déclarer le dosage (en raison de restrictions réglementaires, par exemple) de celles pour lesquelles cela
            ne sera pas nécessaire. Nous vous tiendrons informés dès que cette modification sera effectuée.
            <strong>
              En attendant, si une substance ne nécessite pas de dosage, vous pouvez simplement indiquer zéro.
            </strong>
          </p>
          <p>
            <span aria-hidden="true">💡</span>
            Le bouton "Cliquez pour voir plus d'informations...", identifié par une bulle de texte en couleur bleue,
            <v-icon name="ri-chat-4-line" color="rgb(0, 0, 145)"></v-icon>
            , vous permet d'accéder aux informations disponibles sur chaque ingrédient, telles que la quantité maximale
            autorisée ou les recommandations spécifiques pour certaines populations. Quand l'icône est gris et barrée,
            <v-icon name="ri-chat-off-line" color="#AAA"></v-icon>
            , il n'y a pas des informations supplementaires à afficher.
          </p>
          <p>
            <span aria-hidden="true">🚀</span>
            Dans les prochains mois, nous allons enrichir nos bases de données afin de vous fournir encore plus
            d’informations, pour mieux vous accompagner dans la déclaration de vos produits.
          </p>
        </DsfrAccordion>
        <DsfrAccordion
          title="Comment faire si un ingrédient présent dans mon complément alimentaire n’existe pas sur Compl’Alim ?"
        >
          <p>
            Si un ingrédient de votre complément alimentaire n’existe pas dans Compl’Alim, voici la démarche à suivre :
          </p>
          <ol>
            <li>Cliquez sur le bouton : "Créer un nouvel ingrédient" ;</li>
            <li>
              Remplissez le formulaire pour déclarer ce nouvel ingrédient : spécifiez le type d’ingrédient (plante,
              vitamine, etc.), son nom, sa description, et, dans le cas d’un microorganisme, précisez également son
              genre et son espèce.
            </li>
            <li>
              Un nouvel onglet apparaîtra ensuite pour vous demander si cet ingrédient est autorisé ou utilisable en
              France. Si ce n'est pas le cas et que vous vous appuyez sur le principe de reconnaissance mutuelle, vous
              devrez indiquer dans quel pays de l'UE ou de l'EEE il est utilisé, ainsi que la source réglementaire de
              référence.
            </li>
            <li>
              Si vous souhaitez fournir des pièces justificatives supplémentaires pour soutenir votre déclaration, vous
              pouvez les transmettre dans l'onglet "Pièces jointes".
            </li>
          </ol>
          <p>Vous pouvez créer :</p>
          <ul>
            <li>une nouvelle plante</li>
            <li>une nouvelle partie d’une plante qui existe déjà en base</li>
            <li>un nouveau micro-organisme</li>
            <li>une nouvelle forme d’apport</li>
            <li>un nouvel additif</li>
            <li>un nouvel arôme</li>
            <li>autres ingrédients actifs</li>
            <li>autres ingrédients non actifs</li>
          </ul>
        </DsfrAccordion>
        <DsfrAccordion title="Quid de la distinction article 15/16 du décret n°2006-352 ?">
          <p>
            Vous n’avez désormais plus besoin de déterminer vous-mêmes si le complément alimentaire relève de l'article
            15 ou 16 du décret n°2006-352. L'algorithme de Compl'Alim se charge automatiquement de cette classification
            en fonction de la composition que vous renseignez. Cela simplifie la procédure et garantit une attribution
            conforme aux dispositions réglementaires.
          </p>
        </DsfrAccordion>
        <h2 class="fr-h4">Suivi de l’instruction</h2>
        <DsfrAccordion title="Comment suivre l’état d’avancement de l’instruction de mes dossiers ?">
          <p>
            Dès qu'il y a une évolution ou une actualité concernant votre dossier, vous serez automatiquement averti par
            email. Cela vous permet de rester informé.e en temps réel de toute mise à jour importante.
          </p>
          <p>
            Vous pouvez également accéder à une vue récapitulative cliquant sur la carte "Toutes mes déclarations"
            depuis votre tableau de bord. Vous accédez alors un tableau répertoriant l'ensemble de vos déclarations. Ce
            tableau est partagé avec tous les collaborateurs rattachés à votre entreprise sur Compl’Alim, ce qui vous
            permet de suivre collectivement l’avancement de chaque dossier.
          </p>
          <p>
            <strong>accéder aux détails d'un dossier, cliquez sur le nom du produit dans le tableau</strong>
            .
          </p>
          <p>
            <span aria-hidden="true">💡</span>
            Le filtre "Types de déclaration affichés" vous permet de sélectionner les dossiers que vous souhaitez voir à
            l’écran, en choisissant les types de déclarations qui vous intéressent : Brouillon, Instruction,
            Observation, Objection, Abandon, Déclaration finalisée, Refus, Retiré du marché.
          </p>
        </DsfrAccordion>
        <DsfrAccordion title="Comment récupérer l’attestation d’enregistrement de mon dossier ?">
          <p>
            Une fois votre dossier soumis, vous pouvez télécharger l'accusé d'enregistrement au format PDF. Pour cela :
          </p>
          <ul>
            <li>
              cliquez sur le nom du produit qui vous intéresse dans le tableau récapitulatif ("Toutes mes
              déclarations").
            </li>
            <li>cliquez sur le bouton "Accusé d’enregistrement".</li>
          </ul>
          <p>
            Ce PDF contient l’accusé d’enregistrement de déclaration de votre complément alimentaire ainsi que votre
            engagement de conformité.
          </p>
        </DsfrAccordion>
        <DsfrAccordion title="Comment télécharger le résumé de mon dossier ?">
          <p>
            Actuellement, il n'est pas encore possible de télécharger directement le résumé de votre dossier via la
            plateforme.
          </p>
          <p>En attendant cette fonctionnalité, vous pouvez créer une version PDF en suivant cette méthode :</p>
          <ul>
            <li>rendez-vous sur l’onglet "Résumé"</li>
            <li>effectuez un clic droit avec votre souris</li>
            <li>sélectionnez "Imprimer"</li>
            <li>choisissez l'option "Enregistrer au format PDF" pour obtenir un fichier téléchargeable.</li>
          </ul>
          <p>Et voilà, le tour est joué !</p>
        </DsfrAccordion>
        <DsfrAccordion title="Comment gérer une observation/objection sur votre dossier ?">
          <p>
            Lorsqu’une objection a été émise sur la déclaration de votre produit, vous pouvez consulter les détails en
            vous rendant sur la page dédiée à ce complément alimentaire. Pour cela, cliquez sur le nom du produit qui
            vous intéresse dans le tableau récapitulatif ("Toutes mes déclarations").
          </p>
          <p>
            Les commentaires de l’instructeur, expliquant les raisons de cette observation/objection, seront visibles
            dans l'onglet Historique. Après avoir pris connaissance des remarques, il vous sera nécessaire de soumettre
            une nouvelle version de votre dossier, en tenant compte des éléments supplémentaires ou des modifications
            demandées par l'administration.
          </p>
        </DsfrAccordion>
        <DsfrAccordion
          title="Comment récupérer l’attestation de déclaration d’un produit une fois l’instruction finalisée ?"
        >
          <p>
            Une fois votre dossier instruit, vous pouvez télécharger l’attestation de déclaration au format PDF. Pour
            cela :
          </p>
          <ul>
            <li>
              cliquez sur le nom du produit qui vous intéresse dans le tableau récapitulatif ("Toutes mes
              déclarations").
            </li>
            <li>cliquez sur le bouton "Attestation de déclaration".</li>
          </ul>
          <p>Pour rappel, vous serez informé.e par mail lorsque votre dossier aura été instruit.</p>
        </DsfrAccordion>
        <h2 class="fr-h4">Transition Teleicare/Compl’Alim</h2>
        <DsfrAccordion
          title="Dois-je recréer mon entreprise sur Compl'Alim alors qu'elle est déjà enregistrée sur Teleicare ?"
        >
          <p>Oui, vous devez recréer une fiche pour votre entreprise sur Compl'Alim.</p>
        </DsfrAccordion>
        <DsfrAccordion title="Dois-je redéclarer sur Compl’Alim les produits déclarés sur Teleicare ?">
          <p>
            II ne sera pas nécessaire de déclarer à nouveau sur Compl'Alim les produits que vous avez déjà déclarés sur
            Teleicare.
          </p>
          <p>
            L’historique de vos déclarations antérieures sera importé sur Compl'Alim d’ici la fin de l’année, ce qui
            vous permettra de retrouver toutes vos informations sans avoir à refaire les démarches. Nous ferons le lien
            grâce au SIRET de l'entreprise (après qu'elle ait été créée sur Compl'Alim).
          </p>
          <p>
            En attendant que cela soit fait, vous conserverez l'accès à la rubrique "Je consulte les produits" de
            Teleicare et pourrez donc toujours accéder à vos attestations de déclaration.
          </p>
        </DsfrAccordion>
        <DsfrAccordion
          title="Dois-je resoumettre sur Compl’Alim les dossiers transmis via Teleicare mais pas encore instruits ?"
        >
          <p>
            Les dossiers transmis sur Teleicare seront instruits sur Teleicare. Vous conservez l’accès à la rubrique "Je
            suis mes déclarations" de Teleicare.
          </p>
          <p>
            Une fois votre dossier instruit, l’attestation de déclaration sera importée sur Compl’Alim au moment de
            l’import de l’historique prévu d’ici la fin de l’année (voir question ci-dessus).
          </p>
        </DsfrAccordion>
      </DsfrAccordionsGroup>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
const activeAccordion = ref()
const contactEmail = window.CONTACT_EMAIL
</script>

<style scoped>
@reference "../styles/index.css";

h2 {
  @apply mb-4 mt-6;
}
</style>
