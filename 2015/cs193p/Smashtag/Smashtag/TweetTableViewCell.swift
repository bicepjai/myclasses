//
//  TweetTableViewCell.swift
//  Smashtag
//
//  Created by Jayaram Prabhu Durairaj on 3/8/15.
//  Copyright (c) 2015 bicepjai. All rights reserved.
//

import UIKit

class TweetTableViewCell: UITableViewCell {

    var tweet: Tweet? {
        didSet {
            updateUI()
        }
    }
    
    @IBOutlet weak var tweetScreenNameLabel: UILabel!
    @IBOutlet weak var tweetTextLabel: UILabel!
    @IBOutlet weak var tweetProfileImageView: UIImageView!
    @IBOutlet weak var tweetCreatedLabel: UILabel!
    func updateUI() {
        // reset any existing tweet information
        tweetTextLabel?.attributedText = nil
        tweetScreenNameLabel?.text = nil
        tweetProfileImageView?.image = nil
        tweetCreatedLabel?.text = nil
        
        // load new information from our tweet (if any)
        if let tweet = self.tweet
        {
            if tweetTextLabel?.text != nil  {
                for _ in tweet.media {
                    tweetTextLabel.text! += " 📷"
                }
            }
            
            var attrText = NSMutableAttributedString(string: tweet.text)
            attrText.changeKeywordsColor(tweet.hashtags, color: UIColor.redColor())
            attrText.changeKeywordsColor(tweet.urls, color: UIColor.blueColor())
            attrText.changeKeywordsColor(tweet.userMentions, color: UIColor.orangeColor())
            tweetTextLabel?.attributedText = attrText
            
            tweetScreenNameLabel?.text = "\(tweet.user)" // tweet.user.description
            
            if let profileImageURL = tweet.user.profileImageURL {
                if let imageData = NSData(contentsOfURL: profileImageURL) { // blocks main thread!
                    tweetProfileImageView?.image = UIImage(data: imageData)
                }
            }
            
            let formatter = NSDateFormatter()
            if NSDate().timeIntervalSinceDate(tweet.created) > 24*60*60 {
                formatter.dateStyle = NSDateFormatterStyle.ShortStyle
            } else {
                formatter.timeStyle = NSDateFormatterStyle.ShortStyle
            }
            tweetCreatedLabel?.text = formatter.stringFromDate(tweet.created)
        }
    }
    
    
}

private extension NSMutableAttributedString {
    func changeKeywordsColor(keywords: [Tweet.IndexedKeyword], color: UIColor) {
        for keyword in keywords {
            addAttribute(NSForegroundColorAttributeName, value: color, range: keyword.nsrange)
        }
    }
}
