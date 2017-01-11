//
//  HappinessViewController.swift
//  Happiness
//
//  Created by bicepjai on 2/13/15.
//  Copyright (c) 2015 bicepjai. All rights reserved.
//

import UIKit

class HappinessViewController: UIViewController, FaceViewDataSource {

    private struct Constants {
        static let HappinessGestureScale: CGFloat = 4
    }

    @IBAction func changeHappiness(gesture: UIPanGestureRecognizer) {
        switch gesture.state {
        case .Ended: fallthrough
        case .Changed:
            let translation = gesture.translationInView(faceView)
            let happinessChange = -Int(translation.y/Constants.HappinessGestureScale)
            if happinessChange != 0 {
                happiness += happinessChange
                gesture.setTranslation(CGPointZero, inView: faceView)
            }
        default: break
        }
        
    }
    
    @IBOutlet weak var faceView: FaceView! {
        didSet {
            faceView.dataSource = self
            faceView.addGestureRecognizer(UIPinchGestureRecognizer(target: faceView, action: "scale:"))
        }
    }
    
    var happiness: Int = 50 { // 0 = very sad, 100 = ecstatic
        didSet {
            happiness = min(max(happiness, 0),100)
            println("happiness=\(happiness)")
            updateUI()
        }
    }
    
    func smilinessForFaceView(sender: FaceView) -> Double? {
        return Double(happiness-50)/50
    }
    
    func updateUI() {
        faceView.setNeedsDisplay()
    }
}
