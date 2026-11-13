# Planning rules by region

The permit belongs to the real architect and the municipality. This profile
prepares the file and the exact question for the planning office.

## Belgium

Planning is regional; establish the region first (setting
`property.jurisdictions`, otherwise from the property's address, confirmed):

- **Wallonia** (Code du développement territorial, CoDT): planning permits to
  create a dwelling, divide, change the use; subdivision permits; exempt
  works; regularization; limitation of breaches; planning certificates; the
  regional zoning plan (*plan de secteur*); the regional geoportal.
- **Flanders** (*omgevingsvergunning*, the environmental and planning permit):
  above all the **municipal division regulations**, which are the real filter:
  minimum area, number of units, size of the largest unit. They change from
  one municipality to the next and over time: read the regulation in force,
  with the date of the council decision; a city FAQ is not the regulation.
- **Brussels** (Code bruxellois de l'aménagement du territoire, CoBAT) and its
  planning regulations.
- **Land registry**: plots and plans (the federal land registry portal).
- Fire safety and sanitation, insofar as they condition a separate dwelling:
  fire brigade report, regional minimum standards.

## France

Until the primary source has been read, everything is **TO VERIFY**: the local
urban plan (PLU, on the Géoportail de l'urbanisme), the planning certificate,
the building permit or prior declaration to create dwellings or change use,
division and subdivision, the change of use for furnished tourist lets in
municipalities that require it.

## Plans and takeoffs

Areas (habitable, gross, footprint), volumes, quantities per work item, from
plans, permits or surveys: for this profile and for `property-works-estimator`
(skill `plans-and-takeoffs`).

## Outside this profile

- The cost of bringing a property into compliance: `property-works-estimator`.
- The basic deed, co-ownership, sale by units: `property-notary`.
- Whether dividing is worth it, the margin: `property-investment-partner`.
- A planning breach in dispute, an official report, an appeal:
  `property-lawyer`.
