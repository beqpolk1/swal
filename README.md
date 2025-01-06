# Personal Music Release Tracking System
### (aka Stuff Worth a Listen (SWaL))

## Initial Notes

* Adding Data
    * Manually
    * From web site
    * From web site (batch)
    
* Installing a new web-scraper
    
* Retrieving Suggestions
    * Specify options:
        * Property filters (ranges, keywords, values)
        * Number of recommendations
        * Property preferences - weights or specific thresholds/heuristics
        * Default always search for obtained = false
    * Retrieve & display list of candidates
    
* Browsing All Items
    * View as list
    * Arrows for navigating to next/previous entry (activate via keyboard)
    * Filter by any given field:
        * artist
        * album
        * releaseYear
        * genre
        * interestLevel
        * starred
        * obtained
    
* Updating Data
    * Display entry with editable fields
    * Arrows for navigating to next/previous entry (activate via keyboard)
    * Auto-save upon leaving page/entry
    * Save button
    
* Data Model
```json
{
    artist: String,
    album: String,
    releaseYear: Number,
    genre: String,
    interestLevel: Number,
    starred: Boolean,
    artwork: Blob,
    obtained: Boolean,
    link: String
}
```
    * Interest Level: range [1,3]


## Environment/Deployment Notes
* "Deployment"
    * Initial:
        * Download latest release -> version of github repo
        * Build w/ Docker compose from root dir
        * Run w/ Docker compose
        * Use app; data persisted in Docker volume
        * Tear down Docker containers etc.
    * Repeat:
        * Run w/ Docker compose
        * Use app; data persisted in Docker volume
        * Tear down Docker containers etc.
    * Upgrade:
        * Download latest release -> version of github repo
        * Build w/ Docker compose from root dir
            * Change in structure of persisted data in app (DB or static files)?
            * This would require removing + remaking Docker volumes, which removes data...
            * Would need to provide upgrade scripts to restructure Docker volume contents
            * Upgrade scripts would need to run prior to using application
                * Is it possible to store version info on static volume, auto-compare on container startup, look for + run any needed upgrade scripts?
        * Run w/ Docker compose
        * Use app; data persisted in Docker volume
        * Tear down Docker containers etc.
    * Migrate existing instance to new machine:
        * Follow steps for initial deployment as above
        * Would require migrating Docker volume contents for persisted data to new machine
            * Exec in, mount local volume, copy from Docker volume to local volume, transfer to new machine
            * Repeat process on new machine (copy data from local volume to mounted Docker volume w/in container)
* Environments
    * Feature branches:
        * After testing, pull into dev branch
        * May need to pull dev into feature if feature priority is adjusted
        * Should reference same persisted data (static, DB), same config  as dev branch
    * dev branch:
        * Pools feature branches into complete dev environment
        * Persisted data:
            * Web: App code -> local volume 1 (branch specific)
            * Nginx: Static content (css/js/interface img) -> local volume 2 (branch specific)
            * Nginx: User static content (images) -> local volume 3 **gitignore**
            * DB: DB content -> Docker volume A
        * Config:
            * Web: DB endpoint -> Docker container
            * Web: Static files??
            * Nginx: Static files??
        * After doing integration testing on added features, pull into golden branch
    * golden branch:
        * Final testing before "prod" release
        * Represents "prod" release, but for testing purposes (e.g. recreating bugs)
        * Persisted data:
            * Web: App code -> local volume 1 (branch specific)
            * Nginx: Static content (css/js/interface img) -> local volume 2 (branch specific)
            * Nginx: User static content (images) -> local volume 4 **gitignore**
            * DB: DB content -> Docker volume B
        * Config:
            * Web: DB endpoint -> "external"??
            * Web: Static files??
            * Nginx: Static files??
        * After final functional testing pull golden into prod
    * prod branch:
        * For full prod releases only
        * Persisted data:
            * Web: App code -> copied into container
            * Nginx: Static content (css/js/interface img) -> copied into container
            * Nginx: User static content (images) -> Docker volume C
            * DB: DB content -> Docker volume D
        * Config:
            * Web: DB endpoint -> "external"??
            * Web: Static files??
            * Nginx: Static files??