//
//  PsychologistViewController.swift
//  Psychologist
//
//  Created by bicepjai on 2/23/15.
//  Copyright (c) 2015 bicepjai. All rights reserved.
//

import UIKit

class PsychologistViewController: UIViewController {

    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // identofy the nav controller embedded in
        var destination = segue.destinationViewController as? UIViewController
        if let navCon = destination as? UINavigationController {
            destination = navCon.visibleViewController
        }
        
        if let hvc = destination as? HappinessViewController {
            if let identifier = segue.identifier {
                switch identifier {
                    case "sad"      : hvc.happiness = 0
                    case "happy"    : hvc.happiness = 100
                    case "nothing"  : hvc.happiness = 25
                    default         : hvc.happiness = 50
                }
            }
        }
    }

    @IBAction func nothing(sender: UIButton) {
        performSegueWithIdentifier("nothing", sender: nil)
    }

}

