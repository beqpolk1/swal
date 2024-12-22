## Personal Music Release Tracking System
### (aka Stuff Worth a Listen (SWaL))

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
    