<template>
  <div class="fr-container pb-10">
    <DsfrBreadcrumb :links="[{ to: '/', text: 'Accueil' }, { text: 'Accessibilité' }]" />
    <h1>Déclaration d'accessibilité</h1>
    <p class="italic">Cette déclaration a été établie le 9 septembre 2025</p>
    <p>
      Compl'Alim s’engage à rendre ses services numériques accessibles conformément à l’article 47 de la loi n° 2005-102
      du 11 février 2005.
    </p>
    <p>
      À cette fin, nous mettons en œuvre un schéma pluriannuel présentant la politique en matière d'accessibilité
      numérique (en cours de rédaction) ainsi qu'un plan annuel d'action.
    </p>
    <p>
      Cette déclaration d’accessibilité s’applique au site internet Compl’Alim (
      <a href="https://complements-alimentaires-demo.cleverapps.io/accueil/">
        https://complements-alimentaires-demo.cleverapps.io/accueil/
      </a>
      ).
    </p>
    <h2>État de conformité</h2>
    <p>
      Le site internet Compl’Alim est
      <b>non conforme</b>
      avec le référentiel général d’amélioration de l’accessibilité (RGAA), version 4.1.2 en raison des non-conformités
      énumérées ci-dessous.
    </p>
    <h2>Résultats des tests</h2>
    <p>
      L’audit de conformité réalisé par la société
      <a href="https://www.tanaguru.com">Tanaguru</a>
      le 9 septembre 2025 révèle que :
    </p>
    <ul>
      <li>
        <b>Taux de conformité de l’échantillon audité</b>
        :
        <b>46%</b>
        des critères du RGAA version 4.1.2 sont respectés sur l’ensemble de l’échantillon
        <b>(17 pages)</b>
        .
      </li>
      <li>
        <b>Taux moyen de chaque page</b>
        : Le taux de conformité moyen de chaque page de l’échantillon s’élève à
        <b>68%</b>
        .
      </li>
    </ul>
    <h2>Contenus non accessibles</h2>
    <p>Les contenus listés ci-dessous ne sont pas accessibles pour les raisons suivantes :</p>
    <h3>Non-conformité</h3>
    <h4>Thématique 1 : images</h4>
    <ul>
      <li>
        Critère 1.2 : Certaines images de décoration ne sont pas correctement ignorées par les technologies d'assistance
        ;
      </li>
    </ul>
    <h4>Thématique 3 : Couleurs</h4>
    <ul>
      <li>Critère 3.1 : Certaines informations sont données uniquement par la couleur ;</li>
    </ul>
    <h4>Thématique 5 : Tableaux</h4>
    <ul>
      <li>Critère 5.3 : Pour chaque tableau de mise en forme, le contenu linéarisé ne reste pas compréhensible ;</li>
      <li>Critère 5.4 : Des titres ne sont pas correctement associés au tableau de données ;</li>
      <li>
        Critère 5.6 : Des en-têtes de colonnes ou des en-têtes de lignes de tableau ne sont pas correctement déclarés ;
      </li>
      <li>Critère 5.7 : Les cellules d’en-têtes ne sont pas associées aux cellules correspondantes ;</li>
    </ul>
    <h4>Thématique 6 : Liens</h4>
    <ul>
      <li>Critère 6.1 : Certains liens ne sont pas explicites ;</li>
    </ul>
    <h4>Thématique 7 : Scripts</h4>
    <ul>
      <li>Critère 7.1 : Certains scripts sont incompatibles avec les technologies d’assistance ;</li>
      <li>Critère 7.3 : Certains scripts ne sont pas contrôlables par le clavier ;</li>
      <li>Critère 7.4 : Les utilisateurs ne sont pas avertis des changements de contexte ;</li>
    </ul>
    <h4>Thématique 8 : Éléments obligatoires</h4>
    <ul>
      <li>Critère 8.5 : Certaines pages n’ont pas de titre de page ;</li>
      <li>Critère 8.9 : Certaines balises sont utilisées uniquement à des fins de présentation ;</li>
    </ul>
    <h4>Thématique 9 : Structuration de l’information</h4>
    <ul>
      <li>Critère 9.1 : La hiérarchie des titres n’est pas appropriée ;</li>
      <li>Critère 9.2 : La structure de certaines pages n’est pas cohérente ;</li>
      <li>Critère 9.3 : Certaines listes sont incorrectement structurées dans le code ;</li>
    </ul>
    <h4>Thématique 10 : Présentation de l’information</h4>
    <ul>
      <li>
        Critère 10.1 : Des éléments de présentation sont présents dans le code au lieu d’être sur des feuilles de style
        ;
      </li>
      <li>
        Critère 10.2 : Certains contenus visibles porteurs d’information disparaissent lorsque les feuilles de style
        sont désactivées ;
      </li>
      <li>Critère 10.7 : Le style du focus natif du navigateur est supprimé ou dégradé ;</li>
      <li>Critère 10.8 : Certains contenus cachés devraient être restitués par les technologies d’assistance ;</li>
      <li>
        Critère 10.11 : Certains contenus ne peuvent être présentés sans défilement horizontal sur une fenêtre de 320px
        de large ;
      </li>
      <li>
        Critère 10.12 : Les propriétés d'espacement du texte ne peuvent pas être redéfinies par l'utilisateur sans perte
        de contenu ou de fonctionnalité ;
      </li>
      <li>
        Critère 10.13 : Certains contenus additionnels ne peuvent pas être masqués par l’utilisateur après leur
        apparition ;
      </li>
    </ul>
    <h4>Thématique 11 : Formulaires</h4>
    <ul>
      <li>Critère 11.1 : Certains champs de formulaire n’ont pas d’étiquette ;</li>
      <li>Critère 11.2 : Certaines étiquettes associées à des champs de formulaire ne sont pas pertinentes ;</li>
      <li>
        Critère 11.5 : Certains champs de même nature ne sont pas regroupés dans une balise
        <code>&lt;fieldset&gt;</code>
        ;
      </li>
      <li>Critère 11.6 : Certains regroupements de champs de même nature n’ont pas de légende ;</li>
      <li>
        Critère 11.8 : Les items de même nature d'une liste de choix ne sont pas regroupés de manière pertinente ;
      </li>
      <li>Critère 11.9 : L'intitulé de certains boutons n’est pas pertinent ;</li>
      <li>
        Critère 11.10 : Le contrôle de saisie n’est pas pertinent (Indication des champs obligatoires, exemple de
        type/format de données attendus, message d’erreur nominatif, etc.) ;
      </li>
      <li>
        Critère 11.11 : Le contrôle de saisie n’est pas accompagné de suggestions pour faciliter la correction des
        erreurs de saisie (exemple de type/format de données attendus, message d’erreur pertinent, etc.) ;
      </li>
      <li>
        Critère 11.13 : La finalité de certains champs de saisie ne peut pas être déduite pour faciliter le remplissage
        automatique des champs avec les données de l'utilisateur ;
      </li>
    </ul>
    <h4>Thématique 12 : Navigation</h4>
    <ul>
      <li>Critère 12.8 : Dans chaque page web, l'ordre de tabulation dans le contenu est parfois incohérent ;</li>
    </ul>
    <h4>Thématique 13 : Consultation</h4>
    <ul>
      <li>Critère 13.3 : Certains documents bureautiques ne sont pas accessibles ;</li>
    </ul>
    <h3>Dérogations pour charge disproportionnée</h3>
    <p>Aucune</p>
    <h3>Contenus non soumis à l’obligation d’accessibilité</h3>
    <p>Aucuns</p>
    <h2>Établissement de cette déclaration d’accessibilité</h2>
    <p>Cette déclaration a été établie le 9 septembre 2025.</p>
    <h3>Technologies utilisées pour la réalisation du service</h3>
    <ul>
      <li>HTML 5</li>
      <li>CSS 3</li>
      <li>Javascript</li>
    </ul>
    <h3>Agents utilisateurs, technologies d’assistance et outils utilisés pour vérifier l’accessibilité</h3>
    <p>
      Les tests des pages web ont été effectués avec les combinaisons de navigateurs web et lecteurs d’écran suivantes :
    </p>
    <ul>
      <li>Firefox et NVDA (dernière version) ;</li>
      <li>Safari et VoiceOver (dernière version) ;</li>
      <li>Firefox et Jaws (version précédente).</li>
    </ul>
    <p>Les outils suivants ont été utilisés lors de l’évaluation :</p>
    <ul>
      <li>Outils pour développeurs intégrés au navigateur Firefox ;</li>
      <li>Extension Tanaguru Webext ;</li>
      <li>Extension Web Developer ;</li>
      <li>Extension Stylus ;</li>
      <li>Extension HeadingsMap ;</li>
      <li>Colour Contrast Analyser ;</li>
      <li>Validateur HTML du W3C.</li>
    </ul>
    <p>Pages du site ayant fait l’objet de la vérification de conformité :</p>
    <ul>
      <li>
        Page 1 :
        <a href="https://complements-alimentaires-demo.cleverapps.io/accueil/">Accueil</a>
      </li>
      <li>
        Page 2 :
        <a href="https://complements-alimentaires-demo.cleverapps.io/faq">FAQ</a>
      </li>
      <li>
        Page 3 :
        <a href="https://complements-alimentaires-demo.cleverapps.io/accessibilite">Accessibilité</a>
      </li>
      <li>
        Page 4 :
        <a href="https://complements-alimentaires-demo.cleverapps.io/mentions-legales">Mentions légales</a>
      </li>
      <li>
        Page 5 :
        <a href="https://complements-alimentaires-demo.cleverapps.io/sitemap">Plan du site</a>
      </li>
      <li>
        Page 6 :
        <a href="https://complements-alimentaires-demo.cleverapps.io/contactez-nous">Contact</a>
      </li>
      <li>
        Page 7 :
        <a href="https://complements-alimentaires-demo.cleverapps.io/resultats?q=zinc">Résultats de recherche</a>
      </li>
      <li>
        Page 8 :
        <a href="https://complements-alimentaires-demo.cleverapps.io/element/1792--plante--Test ingrédient%20a11y">
          Fiche ingrédient
        </a>
      </li>
      <li>
        Page 9 :
        <a href="https://complements-alimentaires-demo.cleverapps.io/connexion">Connexion</a>
      </li>
      <li>
        Page 10 :
        <a href="https://complements-alimentaires-demo.cleverapps.io/tableau-de-bord">Tableau de bord</a>
      </li>
      <li>
        Page 11 :
        <a href="https://complements-alimentaires-demo.cleverapps.io/nouvelle-demarche">
          Nouvelle démarche onglet Produit
        </a>
      </li>
      <li>
        Page 12 :
        <a href="https://complements-alimentaires-demo.cleverapps.io/mes-declarations">Mes déclarations</a>
      </li>
      <li>
        Page 13 :
        <a href="https://complements-alimentaires-demo.cleverapps.io/gestion-des-collaborateurs/15">
          Gestion des collaborateurs
        </a>
      </li>
      <li>
        Page 14 :
        <a href="https://complements-alimentaires-demo.cleverapps.io/mes-declarations/164">Déclaration</a>
      </li>
      <li>
        Page 15 :
        <a href="https://complements-alimentaires-demo.cleverapps.io/mes-declarations/167?tab=1">
          Nouvelle démarche onglet Composition
        </a>
      </li>
      <li>
        Page 16 :
        <a href="https://complements-alimentaires-demo.cleverapps.io/mes-declarations/167?tab=2">
          Nouvelle démarche onglet Pièces Jointes
        </a>
      </li>
      <li>
        Page 17 :
        <a href="https://complements-alimentaires-demo.cleverapps.io/mes-declarations/167/?tab=3">
          Nouvelle démarche onglet Soumettre
        </a>
      </li>
    </ul>
    <h2>Retour d’information et contact</h2>
    <p>
      Si vous n’arrivez pas à accéder à un contenu ou à un service, vous nous contacter par email à l'adresse
      <a href="mailto:contact@compl-alim.beta.gouv.fr">contact@compl-alim.beta.gouv.fr</a>
      pour être orienté vers une alternative accessible ou obtenir le contenu sous une autre forme.
    </p>
    <h2>Voie de recours</h2>
    <p>
      Cette procédure est à utiliser dans le cas suivant : vous avez signalé au responsable du site internet un défaut
      d’accessibilité qui vous empêche d’accéder à un contenu ou à un des services du portail et vous n’avez pas obtenu
      de réponse satisfaisante.
    </p>
    <p>Vous pouvez :</p>
    <ul>
      <li>
        Écrire un message au
        <a href="https://formulaire.defenseurdesdroits.fr/">Défenseur des droits</a>
      </li>
      <li>
        Contacter le délégué d
        <a href="https://www.defenseurdesdroits.fr/saisir/delegues">Défenseur des droits dans votre région</a>
      </li>
      <li>
        Envoyer un courrier par la poste (gratuit, ne pas mettre de timbre) :
        <span class="italic">Défenseur des droits Libre réponse 71120 75342 Paris CEDEX 07.</span>
      </li>
    </ul>
  </div>
</template>
