//
//  TweetTableViewController.swift
//  Smashtag
//
//  Created by Jayaram Prabhu Durairaj on 3/7/15.
//  Copyright (c) 2015 bicepjai. All rights reserved.
//

import UIKit

class TweetTableViewController: UITableViewController, UITextFieldDelegate
{

    var tweets = [[Tweet]]()

    @IBOutlet weak var searchTextField: UITextField! {
        didSet {
            searchTextField.delegate = self
            searchTextField.text = searchText
        }
    }
    
    let savedSearches = SavedSearches()

    var searchText: String? = "#stanford" {
        didSet {
            lastSuccessfulRequest = nil
            searchTextField?.text = searchText
            tweets.removeAll()
            tableView.reloadData()
            refresh()
        }
    }
    
    func textFieldShouldReturn(textField: UITextField) -> Bool {
        if textField == searchTextField {
            textField.resignFirstResponder()
            searchText = searchTextField.text
        }
        return true
    }
    
    var lastSuccessfulRequest: TwitterRequest?
    
    var nextRequestToAttempt: TwitterRequest? {
        if lastSuccessfulRequest == nil {
            if searchText != nil {
                return TwitterRequest(search: searchText!, count: 100)
            }
        } else {
            return lastSuccessfulRequest!.requestForNewer
        }
        return nil
    }

    func refresh () {
        if refreshControl == nil {
            refreshControl?.beginRefreshing()
        }
        refresh(refreshControl!)
    }
    
    @IBAction func refresh(sender: UIRefreshControl) {
        if searchText != nil {
            if let request = nextRequestToAttempt {
                request.fetchTweets { (newTweets) -> Void in
                    dispatch_async(dispatch_get_main_queue()) { () -> Void in
                        if newTweets.count > 0 {
                            self.lastSuccessfulRequest = request
                            self.tweets.insert(newTweets, atIndex: 0)
                            self.tableView.reloadData()
                            self.tableView.reloadSections(NSIndexSet(indexesInRange: NSMakeRange(0, self.tableView.numberOfSections())), withRowAnimation: .None)
                            
                        }
                        sender.endRefreshing()
                    }
                }
            }
        } else {
            sender.endRefreshing()
        }
    }
    
    // MARK: - View Controller Life Cycle

    override func viewDidLoad() {
        super.viewDidLoad()
        tableView.estimatedRowHeight = tableView.rowHeight
        tableView.rowHeight = UITableViewAutomaticDimension 
        refresh()
        
        // Uncomment the following line to preserve selection between presentations
        // self.clearsSelectionOnViewWillAppear = false

        // Uncomment the following line to display an Edit button in the navigation bar for this view controller.
        // self.navigationItem.rightBarButtonItem = self.editButtonItem()
    }
    
    // MARK: - UITableViewDataSource

    override func numberOfSectionsInTableView(tableView: UITableView) -> Int {
        // #warning Potentially incomplete method implementation.
        // Return the number of sections.
        return tweets.count
    }

    override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // #warning Incomplete method implementation.
        // Return the number of rows in the section.
        return tweets[section].count
    }

    private struct Storyboard {
        static let CellReuseIdentifier = "TweetCell"
        static let TweetDetailSegue = "TweetDetailSegue"
    }
    
    override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCellWithIdentifier(Storyboard.CellReuseIdentifier, forIndexPath: indexPath) as TweetTableViewCell

        // Configure the cell...
        cell.tweet = tweets[indexPath.section][indexPath.row]
        return cell
    }
    
    override func tableView(tableView: UITableView, estimatedHeightForRowAtIndexPath indexPath: NSIndexPath) -> CGFloat {
        let cell = tableView.dequeueReusableCellWithIdentifier(Storyboard.CellReuseIdentifier, forIndexPath: indexPath) as TweetTableViewCell
        return cell.tweetTextLabel.frame.height + cell.tweetScreenNameLabel.frame.height
    }
    

    // MARK: - Navigation
    
    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // Get the new view controller using [segue destinationViewController].
        // Pass the selected object to the new view controller.
        // identify the nav controller embedded in
        var destination = segue.destinationViewController as? UIViewController
        if let navCon = destination as? UINavigationController {
            destination = navCon.visibleViewController
        }
        
        let indexPath = self.tableView.indexPathForSelectedRow()!
        let cell = tableView.cellForRowAtIndexPath(indexPath) as TweetTableViewCell
        
        if let tvc = destination as? TweetDetailsTableViewController {
            if let identifier = segue.identifier {
                switch identifier {
                case Storyboard.TweetDetailSegue  : tvc.tweet = cell.tweet
                default                  : tvc.tweet = nil
                }
            }
        }
    }
    
    override func shouldPerformSegueWithIdentifier(identifier: String?, sender: AnyObject?) -> Bool {
        if identifier == Storyboard.TweetDetailSegue {
            if let tweetCell = sender as? TweetTableViewCell {
                if tweetCell.tweet!.hashtags.count + tweetCell.tweet!.urls.count + tweetCell.tweet!.userMentions.count > 0 {
                    return true
                }
            }
        }
        return false
    }

}
