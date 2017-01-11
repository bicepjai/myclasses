//
//  SavedTableViewController.swift
//  Smashtag
//
//  Created by Jayaram Prabhu Durairaj on 3/21/15.
//  Copyright (c) 2015 bicepjai. All rights reserved.
//

import UIKit

class SavedTableViewController: UITableViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        self.tableView.reloadData()
    }
    
    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)
        self.tableView.reloadData()
    }
    let savedSearches = SavedSearches()
    
    private struct Storyboard {
        static let KeywordCellReuseIdentifier   = "TweetSearchCell"
        static let SegueSavedSearchToTweetTable = "SavedSearchToTweetTable"
        static let SavedSectionHeading          = "Saved Searches"
        static let SegueGotoNavTabSearchTT      = "GotoNavTabSearchTT"
    }
    
    // MARK: - Table view data source

    override func numberOfSectionsInTableView(tableView: UITableView) -> Int {
        // #warning Potentially incomplete method implementation.
        // Return the number of sections.
        return 1
    }

    override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // #warning Incomplete method implementation.
        // Return the number of rows in the section.
        return savedSearches.getSearchHistory().count
    }

    override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCellWithIdentifier(Storyboard.KeywordCellReuseIdentifier, forIndexPath: indexPath) as TweetSearchTableViewCell
        cell.tweetKeyword = savedSearches.getSearchHistory()[indexPath.row]
        return cell
    }

    override func tableView(tableView: UITableView, estimatedHeightForRowAtIndexPath indexPath: NSIndexPath) -> CGFloat {
            let cell = tableView.dequeueReusableCellWithIdentifier(Storyboard.KeywordCellReuseIdentifier, forIndexPath: indexPath) as TweetSearchTableViewCell
            return cell.tweetSearch.frame.height
    }
    
    override func tableView(tableView: UITableView, titleForHeaderInSection section: Int) -> String? {
        return Storyboard.SavedSectionHeading
    }

    // MARK: - Navigation

    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        var destination = segue.destinationViewController as? UIViewController
        if let navCon = destination as? UINavigationController {
            destination = navCon.visibleViewController
        }
        
        if let identifier = segue.identifier {
            switch identifier {
            case Storyboard.SegueSavedSearchToTweetTable:
                if let tvc = destination as? TweetTableViewController {
                    if let cell = sender as? TweetSearchTableViewCell {
                        tvc.searchText = cell.tweetSearch?.text
                        savedSearches.addToSearchHistory((cell.tweetSearch?.text)!)
                    }
                }
            default: break
            }
        }
    }

}
