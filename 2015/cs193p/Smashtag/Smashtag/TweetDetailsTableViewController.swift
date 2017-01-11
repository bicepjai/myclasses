//
//  TweetDetailsTableViewController.swift
//  Smashtag
//
//  Created by Jayaram Prabhu Durairaj on 3/17/15.
//  Copyright (c) 2015 bicepjai. All rights reserved.
//

import UIKit

class TweetDetailsTableViewController: UITableViewController {

    var tweet: Tweet? {
        didSet {
            if let hashtags = tweet?.hashtags {
                if(hashtags.count > 0) {
                    mentions.append(Mention(title: "#Hashtags", color: UIColor.redColor(), data: hashtags.map { TweetDetails.Keyword($0.keyword) }))
                }
            }
            if let userMentions = tweet?.userMentions {
                if(userMentions.count > 0) {
                    mentions.append(Mention(title: "@UserMentions", color: UIColor.blueColor(),data: userMentions.map { TweetDetails.Keyword($0.keyword) }))
                }
            }
            if let urls = tweet?.urls {
                if(urls.count > 0) {
                    mentions.append(Mention(title: "URLs", color: UIColor.orangeColor(), data: urls.map { TweetDetails.Keyword($0.keyword) }))
                }
            }
            if let media = tweet?.media {
                if(media.count > 0) {
                    mentions.append(Mention(title: "Images", color: nil, data: media.map { TweetDetails.Image($0.url, $0.aspectRatio) }))
                }
            }
        }
    }
    
    var mentions:[Mention] = []
    
    struct Mention {
        var title: String?
        var color:UIColor?
        var data:[TweetDetails]
        var description: String { return "\(title): \(data)" }
    }
    
    enum TweetDetails: Printable
    {
        case Keyword(String)
        case Image(NSURL, Double)
        
        var description: String {
            get {
                switch self {
                case .Keyword(let keyword):
                    return ("\(keyword)")
                case .Image(let url, let aspectRatio):
                    return("\(url.description):\(aspectRatio.description)")
                }
            }
        }
    }
    
    let savedSearches = SavedSearches()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        tableView.estimatedRowHeight = tableView.rowHeight
        tableView.rowHeight = UITableViewAutomaticDimension
        refresh()
    }

    func refresh() {
        self.tableView.reloadData()
        self.tableView.reloadSections(NSIndexSet(indexesInRange: NSMakeRange(0, self.tableView.numberOfSections())), withRowAnimation: .None)
    }
    
    // MARK: - Table view data source

    override func numberOfSectionsInTableView(tableView: UITableView) -> Int {
        return mentions.count
    }

    override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return mentions[section].data.count
    }

    private struct Storyboard {
        static let KeywordCellReuseIdentifier   = "TweetKeywordCell"
        static let ImageCellReuseIdentifier     = "TweetImageCell"
        static let SegueToImageInScrollView     = "ImageInScrollView"
        static let SegueSearchForKeywordAgain   = "SearchForKeywordAgain"
        static let URLSectionHeader             = "URLs"
    }
    
    override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        switch mentions[indexPath.section].data[indexPath.row] {
        case TweetDetails.Keyword(let keyword):
            let cell = tableView.dequeueReusableCellWithIdentifier(Storyboard.KeywordCellReuseIdentifier, forIndexPath: indexPath) as TweetKeywordTableViewCell
            cell.tweetKeyword = keyword
            cell.color = mentions[indexPath.section].color!
            return cell
        case TweetDetails.Image(let url, let aspectRatio):
            let cell = tableView.dequeueReusableCellWithIdentifier(Storyboard.ImageCellReuseIdentifier, forIndexPath: indexPath) as TweetImageTableViewCell
            cell.imageURL = url
            return cell
        }

    }

    override func tableView(tableView: UITableView, estimatedHeightForRowAtIndexPath indexPath: NSIndexPath) -> CGFloat {
        switch mentions[indexPath.section].data[indexPath.row] {
        case TweetDetails.Image(let url, let aspectRatio):
            let cell = tableView.dequeueReusableCellWithIdentifier(Storyboard.ImageCellReuseIdentifier, forIndexPath: indexPath) as TweetImageTableViewCell
            return tableView.bounds.size.width / CGFloat(aspectRatio)
        default: break
        }
        return UITableViewAutomaticDimension
    }
    
    override func tableView(tableView: UITableView, titleForHeaderInSection section: Int) -> String? {
        return mentions[section].title
    }
    
    // MARK: - Navigation
    
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        var destination = segue.destinationViewController as? UIViewController
        if let navCon = destination as? UINavigationController {
            destination = navCon.visibleViewController
        }
        
        if let identifier = segue.identifier {
            switch identifier {
            case Storyboard.SegueSearchForKeywordAgain  :
                if let tvc = destination as? TweetTableViewController {
                    if let cell = sender as? TweetKeywordTableViewCell {
                        tvc.searchText = cell.tweetDetail?.text
                        savedSearches.addToSearchHistory((cell.tweetDetail?.text)!)
                    }
                }
            default: break
            }
        }
    }
    
    override func shouldPerformSegueWithIdentifier(identifier: String?, sender: AnyObject?) -> Bool {
        if identifier == Storyboard.SegueSearchForKeywordAgain {
                if let cell = sender as? TweetKeywordTableViewCell {
                    if let keyword = cell.tweetDetail?.text {
                        if keyword.hasPrefix("http") {
                            UIApplication.sharedApplication().openURL(NSURL(string: keyword)!)
                            return false
                        }
                    }
                }
        }
        return true
    }

}
