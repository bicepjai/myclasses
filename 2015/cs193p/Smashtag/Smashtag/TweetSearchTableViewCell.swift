//
//  TweetSearchTableViewCell.swift
//  Smashtag
//
//  Created by Jayaram Prabhu Durairaj on 3/22/15.
//  Copyright (c) 2015 bicepjai. All rights reserved.
//

import UIKit

class TweetSearchTableViewCell: UITableViewCell {
    var tweetKeyword: String? { didSet { updateUI() } }
    
    @IBOutlet weak var tweetSearch: UILabel!
    var color:UIColor = UIColor.blackColor() { didSet { updateUI() } }

    func updateUI() {
        tweetSearch?.text = nil
        
        // load new information from our tweet (if any)
        if let tweetKeyword = self.tweetKeyword
        {
            var attrText = NSMutableAttributedString(string: tweetKeyword)
            attrText.addAttribute(NSForegroundColorAttributeName, value: color, range: NSMakeRange(0, attrText.length) )
            tweetSearch?.attributedText = attrText
        }    }
}
