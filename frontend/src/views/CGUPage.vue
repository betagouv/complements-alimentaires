<template>
  <div class="fr-container pb-10">
    <DsfrBreadcrumb :links="[{ to: '/', text: 'Accueil' }, { text: 'Conditions générales d\'utilisation' }]" />
    <h1>Conditions générales d'utilisation</h1>
    <p>
      Les présentes conditions d’utilisation (CGU) sont mises en œuvre conformément à l’article L. 112-9 du code des
      relations entre le public et l’administration. Elles s’imposent aux usagers.
    </p>
    <h2>Présentation</h2>
    <p>
      « Compl'Alim » (ci-après dénommé « le Service ») est mis en œuvre par le ministère de l’Agriculture et de la
      Souveraineté Alimentaire qui s’appuie sur l’expertise de la Direction interministérielle du numérique dans le
      cadre d’une délégation de gestion.
    </p>
    <p>
      Le Service est destiné à accompagner les acteurs du secteur des compléments alimentaires (ci-après abrégé « CA »)
      en facilitant la constitution des dossiers de déclaration.
    </p>
    <h2>Parcours usagers</h2>
    <p>Le Service est une plateforme numérique permettant :</p>
    <ul>
      <li>la constitution d’un dossier permettant de déclarer un CA,</li>
      <li>la modification d’un produit ou son arrêt de commercialisation,</li>
      <li>la recherche sur l'état d'un produit par le grand public à partir de data.gouv.fr,</li>
      <li>
        la recherche sur l'état d'un produit et sa composition par la DGAL, ses services déconcentrés et ses services à
        compétence nationale ainsi que par l'Anses
      </li>
    </ul>
    <p>Un parcours « instructeur / instructrice » est prévu pour faciliter l’analyse des déclarations.</p>

    <p>
      La création du compte peut être faite directement par l’équipe chargée du Service ou par l’usager. Le compte
      nécessite un mot de passe et permet également l'utilisation d'un lien d’accès envoyé à l’adresse e-mail
      renseignée.
    </p>
    <h2>Mentions légales</h2>
    <ul>
      <li>Éditeur : L'Incubateur de services numériques de la Direction Interministérielle du Numérique (DINUM).</li>
      <li>Directeur de la publication : Ministère de l’Agriculture et de la Souveraineté Alimentaire.</li>
      <li>Prestataire d'hébergement : Clevercloud, 3 rue de l'Allier, 44000 Nantes, France.</li>
    </ul>
    <p>
      Plus d'informations sur nos
      <router-link :to="{ name: 'LegalNoticesPage' }">page dédiée aux mentions légales.</router-link>
    </p>
    <h2>Modalités d’utilisation du Service</h2>
    <p>L'utilisation du Service est facultative et gratuite.</p>
    <p>
      Le Service dépose des cookies de mesure d’audience (nombre de visites, pages consultées), respectant les
      conditions d’exemption du consentement de l’internaute définies par la recommandation « Cookies » de la Commission
      nationale informatique et libertés (CNIL); il utilise Matomo, un outil libre, paramétré pour ce faire. Cela
      signifie, notamment, que ces cookies ne servent qu’à la production de statistiques anonymes et ne permettent pas
      de suivre la navigation de l’internaute sur d’autres sites.
    </p>
    <p>Le Service dépose des cookies de navigation à des fins strictement techniques, qui ne sont pas conservés.</p>
    <h2>Traitement des données</h2>
    <p>
      Le Service ne collecte que les données strictement nécessaires à sa mise en œuvre. Les données collectées incluent
      également des données à caractère personnel.
    </p>
    <p>Les données traitées sont les suivantes :</p>
    <ul>
      <li>
        les données obligatoires pour la création du compte : nom, prénom, nom d'utilisateur, adresse e-mail.
        L’utilisateur doit également fournir les données de l’établissement concerné (par exemple SIRET), qui ne sont
        pas considérées comme des données à caractère personnel.
      </li>
      <li>
        les données facultatives : l’ensemble des champs décrivant la composition des CA. L’équipe chargée du Service se
        réserve néanmoins le droit de supprimer ou de proposer une modification lorsque le contenu proposé ne répond à
        des critères minimaux de qualité.
      </li>
    </ul>
    <p>
      Les données relatives à l’établissement ainsi que les données facultatives relatives aux diagnostics sont
      conservées jusqu’à la fin de fonctionnement du Service, notamment pour répondre aux besoins statistiques.
    </p>
    <p>
      Le ministère de l’Agriculture et de la Souveraineté Alimentaire s'engage à prendre toutes précautions utiles pour
      préserver la sécurité des données collectées auprès de l'usager, et notamment empêcher qu'elles soient déformées
      et endommagées ou que des tiers non autorisés y aient accès.
    </p>
    <p>
      Le ministère de l’Agriculture et de la Souveraineté Alimentaire garantit aux usagers du Service les droits
      d'accès, de rectification et d'opposition sur leurs données à caractère personnel, prévus par la loi n° 78-17 du 6
      janvier 1978 relative à l'informatique aux fichiers et aux libertés.
    </p>
    <p>
      Pour plus d’informations sur le traitement des données à caractère personnel l’utilisateur est invité à se référer
      à la
      <router-link :to="{ name: 'PrivacyPolicyPage' }">politique de confidentialité.</router-link>
    </p>
    <p>
      La validation des CGU implique l’inscription automatique à l’infolettre Compl'Alim. Conforment à la
      réglementation, cette inscription est révocable à tout moment, soit en vous désabonnant à réception du courriel,
      ou en nous notifiant votre refus à l’adresse suivante :
      <a href="mailto:compl-alim@beta.gouv.fr">compl-alim@beta.gouv.fr</a>
    </p>
    <h2>Statistiques</h2>
    <p>Les données récoltées dans le cadre du téléservice servent au pilotage de la politique publique.</p>
    <p>
      Conformément aux dispositions des articles L. 230-5-1 et R. 230-30-4 du Code rural, les données recueillies par
      l’intermédiaire de la plateforme permettent de réaliser un bilan de la mise en œuvre du dispositif qui est adressé
      notamment au Parlement.
    </p>
    <p>
      En outre, conformément aux dispositions du Livre III du Code des relations entre le public et l’administration, la
      plateforme diffuse des informations publiques relatives aux données collectées et au suivi de l’usage de la
      plateforme.
    </p>
    <h2>Engagements et responsabilité</h2>
    <p>
      Le présent Service est mis en œuvre selon les dispositions du code des relations entre le public et
      l’administration (CRPA).
    </p>
    <p>
      Le Service a été développé sous licence MIT , le code est disponible à l’adresse suivante :
      <a href="https://github.com/betagouv/complements-alimentaires/" target="_blank" rel="noopener">
        https://github.com/betagouv/complements-alimentaires/
      </a>
    </p>
    <p>
      Le Service est mis à disposition sans autres garanties expresses ou tacites que celles qui sont prévues par les
      présentes.
    </p>
    <p>
      Le Service est développé conformément à l’état de l’art. Toutefois, il n’est pas garanti qu’il soit exempt
      d’anomalies ou d'erreurs. Le service est donc mis à disposition sans garantie sur sa disponibilité et ses
      performances. A ce titre, le ministère de l’Agriculture et de la Souveraineté Alimentaire ne peut être tenu
      responsable des pertes et/ou préjudices, de quelque nature qu’ils soient, qui pourraient être causés à la suite
      d’un dysfonctionnement ou une indisponibilité du service. De telles situations n'ouvriront droit à aucune
      compensation financière.
    </p>
    <p>
      L’utilisateur s’engage à respecter les présentes CGU et la législation en vigueur. Il s’engage notamment à ne
      fournir, dans le cadre de l'utilisation du Service, que des informations exactes, à jour et complètes.
    </p>
    <p>
      Dans l'hypothèse où l'usager ne s'acquitte pas de ses engagements, le ministère de l’Agriculture et de la
      Souveraineté Alimentaire se réserve le droit de suspendre ou résilier le service pour cet usager sans préjudice
      des éventuelles actions en responsabilité pénale et civile qui pourraient être engagées à son encontre.
    </p>
    <h2>Modification et évolution du Service</h2>
    <p>
      Les termes des présentes conditions d’utilisation peuvent être modifiés ou complétés à tout moment, sans préavis,
      en fonction des modifications apportées au Service, de l’évolution de la législation ou pour tout autre motif jugé
      nécessaire. Ces modifications et mises à jour s’imposent à l’utilisateur qui doit, en conséquence, se référer
      régulièrement à cette rubrique pour vérifier les conditions générales en vigueur.
    </p>
    <h2>Nous contacter</h2>
    <ul>
      <li>
        Difficultés techniques :
        <a href="mailto:compl-alim@beta.gouv.fr">compl-alim@beta.gouv.fr</a>
      </li>
      <li>
        Problèmes liés à la procédure :
        <a href="mailto:compl-alim@beta.gouv.fr">compl-alim@beta.gouv.fr</a>
      </li>
      <li>
        Droit d’accès CNIL :
        <a href="mailto:compl-alim@beta.gouv.fr">compl-alim@beta.gouv.fr</a>
      </li>
    </ul>
  </div>
</template>
