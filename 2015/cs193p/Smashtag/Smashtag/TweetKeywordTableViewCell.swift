//
//  TweetKeywordTableViewCell.swift
//  Smashtag
//
//  Created by Jayaram Prabhu Durairaj on 3/19/15.
//  Copyright (c) 2015 bicepjai. All rights reserved.
//

import UIKit

class TweetKeywordTableViewCell: UITableViewCell {
    
    var tweetKeyword: String? { didSet { updateUI() } }
    
    var color:UIColor = UIColor.blackColor() { didSet { updateUI() } }

    @IBOutlet weak var tweetDetail: UILabel!

    func updateUI() {
        tweetDetail?.text = nil
        
        // load new information from our tweet (if any)
        if let tweetKeyword = self.tweetKeyword
        {
            var attrText = NSMutableAttributedString(string: tweetKeyword)
            attrText.addAttribute(NSForegroundColorAttributeName, value: color, range: NSMakeRange(0, attrText.length) )
            tweetDetail?.attributedText = attrText
        }
    }
}