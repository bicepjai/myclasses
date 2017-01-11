//
//  GraphViewController.swift
//  Calculator
//
//  Created by Jayaram Prabhu Durairaj on 3/8/15.
//  Copyright (c) 2015 bicepjai. All rights reserved.
//

import UIKit

class GraphViewController: UIViewController, GraphViewDataSource, UIPopoverPresentationControllerDelegate {

    private struct Details {
        static let SegueIdentifier = "GraphDetails"
    }
    
    var programFromCalc: AnyObject? {
        didSet {
            updateUI()
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        NSNotificationCenter.defaultCenter().addObserver(self, selector: "updateUI", name: UIDeviceOrientationDidChangeNotification, object: nil)
        // Do any additional setup after loading the view.
    }

    func updateUI() {
        graphView?.setNeedsDisplay()
    }

    let brain = CalculatorBrain()
    
    @IBOutlet weak var graphView: GraphView! {
        didSet {
            graphView.dataSource = self
            graphView.updateDetails()
            graphView.addGestureRecognizer(UIPinchGestureRecognizer(target: graphView, action: "scale:"))
            graphView.addGestureRecognizer(UIPanGestureRecognizer(target: graphView, action: "moveOrigin:"))
            let tapGesture = UITapGestureRecognizer(target: graphView, action: "changeOrigin:")
            tapGesture.numberOfTapsRequired = 2
            graphView.addGestureRecognizer(tapGesture)
        }
    }
    
    func yForX(sender: GraphView, x: CGFloat) -> CGFloat? {
        if let program = programFromCalc as? Array<String> {
            brain.variableValues["M"] = Double(x)
            brain.program = program
            if let result = brain.evaluate() {
                title = brain.description
                switch result {
                case .Value(let y): return CGFloat(y)
                default: break
                }
            }
        }
        return nil
    }

    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        
        if let identifier = segue.identifier {
            switch identifier {
            case Details.SegueIdentifier :
                if let tvc = segue.destinationViewController as? GraphTextViewController {
                    if let ppc = tvc.popoverPresentationController {
                        ppc.delegate = self
                    }
                    tvc.text = "\((graphView?.graphDetails)!))"
                }
            default: break
            }
        }
    }
    
    func adaptivePresentationStyleForPresentationController(controller: UIPresentationController) -> UIModalPresentationStyle {
        return UIModalPresentationStyle.None
    }
}
