//
//  DiagnosedHappinessViewController.swift
//  Psychologist
//
//  Created by bicepjai on 2/23/15.
//  Copyright (c) 2015 bicepjai. All rights reserved.
//

import Foundation
import UIKit

class DiagnosedHappinessViewController: HappinessViewController, UIPopoverPresentationControllerDelegate
{
    private let defaults = NSUserDefaults.standardUserDefaults()
    var diagnosticHistory: [Int] {
        get {
            return defaults.objectForKey(History.DefaultsKey) as? [Int] ?? []
        }
        set { 
            defaults.setObject(newValue, forKey:History.DefaultsKey)
        }
    }
    
    override var happiness: Int {
        didSet {
            diagnosticHistory += [happiness]
        }
    }
    private struct History {
        static let SegueIdentifier = "Show Diagnostic History"
        static let DefaultsKey = "DiagnosedHappinessViewController.History"
    }
    
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        
        if let identifier = segue.identifier {
            switch identifier {
            case History.SegueIdentifier :
                if let tvc = segue.destinationViewController as? TextViewController {
                    if let ppc = tvc.popoverPresentationController {
                        ppc.delegate = self
                    }
                    tvc.text = "\(diagnosticHistory)"
                }
            default: break
            }
        }
    }
    
    func adaptivePresentationStyleForPresentationController(controller: UIPresentationController) -> UIModalPresentationStyle {
        return UIModalPresentationStyle.None
    }
}