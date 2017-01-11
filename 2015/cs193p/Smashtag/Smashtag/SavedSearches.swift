//
//  SavedSearches.swift
//  Smashtag
//
//  Created by Jayaram Prabhu Durairaj on 3/21/15.
//  Copyright (c) 2015 bicepjai. All rights reserved.
//

import Foundation

class SavedSearches {
    
    private struct SearchHistory {
        static let SearchDB         = "Search.History"
        static let SearchIndex      = "Search.Index"
        static let SearchLimit      = 10
        
    }
    
    private let defaults = NSUserDefaults.standardUserDefaults()
    private var searchHistory = [String]()
    
    func addToSearchHistory(keyword: String?) -> Void {
        if keyword != nil {
            searchHistory = getSearchHistory()
            if searchHistory.count == SearchHistory.SearchLimit {
                searchHistory.removeAtIndex(0)
            }
            searchHistory.append(keyword!)
            defaults.setObject(searchHistory, forKey:SearchHistory.SearchDB)
        }
    }
    
    func getSearchHistory() -> [String] {
        return defaults.objectForKey(SearchHistory.SearchDB) as? [String] ?? [String]()
    }
}