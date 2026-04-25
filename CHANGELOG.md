# Changelog

## [1.0.0](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/tree/1.0.0) (2024-11-16)

[Full Changelog](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/compare/0.3.0...1.0.0)

**Closed issues:**

- \[FEAT\] Add version route to api [\#42](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/issues/42)
- \[DOC\] Update description on  pyproject.toml to not have reference to react app. [\#37](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/issues/37)
- \[INFRA\] Create YTT files and deploy to k8s cluster [\#28](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/issues/28)
- \[DOC\] Update README.md with GraphQL queries we support and how to use the api [\#20](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/issues/20)
- \[FEAT\] Add ability to setup CORS reponse and default to \* [\#18](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/issues/18)
- \[INFRA\] Have the tests and docs runs in seperate workflows using artifacts. [\#13](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/issues/13)

**Merged pull requests:**

- feat\(api\): Add version endpoint [\#47](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/47) ([gxldCptRick](https://github.com/gxldCptRick))
- docs\(pypi\): Update Description to remove reference to react frontend. [\#46](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/46) ([gxldCptRick](https://github.com/gxldCptRick))
- feat\(Configuration\): 18 feat add ability to setup cors reponse and default to [\#45](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/45) ([vCertxfiedGoat](https://github.com/vCertxfiedGoat))
- build\(main\): Separate the docs and testing into unique jobs. [\#44](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/44) ([gxldCptRick](https://github.com/gxldCptRick))
- docs\(Readme\): Readme now has graphql queries and outputs [\#36](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/36) ([vCertxfiedGoat](https://github.com/vCertxfiedGoat))
- chore\(changelog\): Updating Changelog for version 0.3.0 [\#35](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/35) ([github-actions[bot]](https://github.com/apps/github-actions))

## [0.3.0](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/tree/0.3.0) (2024-11-15)

[Full Changelog](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/compare/0.2.2...0.3.0)

**Merged pull requests:**

- build\(k8s\): Trying to fix the version check [\#34](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/34) ([gxldCptRick](https://github.com/gxldCptRick))
- build\(k8s\): Adding new workflow to open pr on our flux repo when we want to deploy new versions of the code. [\#33](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/33) ([gxldCptRick](https://github.com/gxldCptRick))
- chore\(changelog\): Updating Changelog for version 0.2.2 [\#31](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/31) ([github-actions[bot]](https://github.com/apps/github-actions))

## [0.2.2](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/tree/0.2.2) (2024-11-14)

[Full Changelog](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/compare/0.2.1...0.2.2)

**Merged pull requests:**

- build\(changelog\): FIxing Changelog to make sure it excludes the dev tags and only does diffs on release tags.  [\#30](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/30) ([gxldCptRick](https://github.com/gxldCptRick))
- build\(k8s\): Adding yaml files and new commands to build app with ytt [\#29](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/29) ([gxldCptRick](https://github.com/gxldCptRick))
- chore\(changelog\): Updating Changelog for version 0.2.1 [\#27](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/27) ([github-actions[bot]](https://github.com/apps/github-actions))

## [0.2.1](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/tree/0.2.1) (2024-11-14)

[Full Changelog](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/compare/0.2.0...0.2.1)

**Closed issues:**

- \[INFRA\] Add the workflows to publish to the org k8s cluster [\#15](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/issues/15)

**Merged pull requests:**

- build\(pypi\): Setting version manually so it does not need to worry about git tags. [\#26](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/26) ([gxldCptRick](https://github.com/gxldCptRick))
- build\(docker\): Fixing version resolution for build. [\#25](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/25) ([gxldCptRick](https://github.com/gxldCptRick))

## [0.2.0](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/tree/0.2.0) (2024-11-14)

[Full Changelog](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/compare/0.1.0...0.2.0)

**Closed issues:**

- \[INFRA\] Create a docker image for the app [\#14](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/issues/14)
- \[FEAT\] add ui to mess with graphql endpoints  [\#9](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/issues/9)
- \[FEAT\] Use GraphQL for main logical endpoints. [\#5](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/issues/5)
- \[FEAT\] Create routes to play the game and do actions on it. [\#4](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/issues/4)
- \[FEAT\] Add routes to create an active game session. [\#3](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/issues/3)

**Merged pull requests:**

- build\(docker\): Add Docker Build workflow for release publishers. [\#24](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/24) ([gxldCptRick](https://github.com/gxldCptRick))
- feat\(graphql\): Added the ability to end a round and draw dice [\#22](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/22) ([vCertxfiedGoat](https://github.com/vCertxfiedGoat))
- feat\(infra\): Adding docker specific files and making it runnable in containers. [\#21](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/21) ([gxldCptRick](https://github.com/gxldCptRick))
- style: Understanding the repo [\#19](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/19) ([vCertxfiedGoat](https://github.com/vCertxfiedGoat))
- fix\(docs\): Fixing pdoc issues that were introduced to main. [\#17](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/17) ([gxldCptRick](https://github.com/gxldCptRick))
- feat\(game\): Adding new routes in graphql to support starting and reading game data. [\#12](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/12) ([gxldCptRick](https://github.com/gxldCptRick))
- feat\(graphql\): Use Graphql for endpoints [\#11](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/11) ([gxldCptRick](https://github.com/gxldCptRick))
- chore\(versioning\): Reverting back to scm but making it work this time for reals. [\#10](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/10) ([gxldCptRick](https://github.com/gxldCptRick))
- chore\(build\): Adding install script [\#8](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/8) ([gxldCptRick](https://github.com/gxldCptRick))
- chore\(versioning\): Update the versioning for the pip package to be reading from \_\_version\_\_ [\#6](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/6) ([gxldCptRick](https://github.com/gxldCptRick))
- chore\(changelog\): Updating Changelog for version 0.1.0 [\#1](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/pull/1) ([github-actions[bot]](https://github.com/apps/github-actions))

## [0.1.0](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/tree/0.1.0) (2024-10-10)

[Full Changelog](https://github.com/Carrera-Dev-Consulting/zombie-nomnom-api/compare/78b08b2c773b841f34659ca7af298356d417e60b...0.1.0)



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
