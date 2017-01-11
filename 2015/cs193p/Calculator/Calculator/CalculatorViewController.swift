//
//  CalculatorViewController
//  calculator
//
//  Created by bicepjai on 1/30/15.
//  Copyright (c) 2015 bicepjai. All rights reserved.
//

import UIKit

class CalculatorViewController: UIViewController {

    @IBOutlet weak var display: UILabel!
    @IBOutlet weak var historyLabel: UILabel!
    
    var userIsTyping: Bool = false
    
    var brain = CalculatorBrain()
    
    @IBAction func appendDigit(sender: UIButton) {
        let digit = sender.currentTitle!
        if(userIsTyping) {
            if digit != "." || display.text?.rangeOfString(".") == nil {
                display.text = display.text! + digit
            }
        } else  {
            if digit == "." {
                display.text = "0."
            } else  {
                display.text = digit
            }
            userIsTyping = true
        }
    }

    @IBAction func resetCE(sender: AnyObject) {
        userIsTyping = false
        brain.clearCalcBrain()
        displayValue = 0
        updateHistoryLabel()
    }
    
    @IBAction func deleteChar(sender: UIButton) {
        
        if userIsTyping {
            if var displayText = display.text {
                if countElements(displayText) > 1 {
                    display.text = dropLast(displayText)
                } else {
                    display.text = "0"
                    userIsTyping = false
                }
            }
        } else {
            if let result = brain.undo() {
                switch result {
                case .Value(let val):
                    displayValue = val
                case .Error(let err):
                    display.text = err
                }
            } else {
                displayValue = 0
            }
            updateHistoryLabel()
        }
    }
    
    @IBAction func enter() {
        userIsTyping = false
        if let dValue = displayValue {
            if let result = brain.pushOperand(dValue) {
                switch result {
                case .Value(let val):
                    displayValue = val
                case .Error(let err):
                    display.text = err
                }            } else {
                displayValue = 0
            }
            updateHistoryLabel()
        } else {
            displayValue = 0
        }
    }
    
    func updateHistoryLabel() {
        if let desc = brain.description {
            if let dV = displayValue {
                historyLabel.text = "\(desc)=\(dV)"
            } else {
                historyLabel.text = "\(desc)= ???"                
            }
        }
    }
    
    var displayValue: Double? {
        get {
            if let dValue = NSNumberFormatter().numberFromString(display.text!) {
                return dValue.doubleValue
            } else {
                return nil
            }
            
        }
        set {
            if let nVal = newValue {
                display.text = "\(nVal)"
                userIsTyping = false
            } else {
                display.text = "0"
            }
        }
    }
    
    @IBAction func setMem(sender: UIButton) {
        brain.setMemory("M",mem: displayValue!)
        userIsTyping = false
    }
    
    
    @IBAction func useMem(sender: UIButton) {
        if let mem = brain.getMemory("M") {
            displayValue = mem
            if let result = brain.pushOperand("M") {
                switch result {
                case .Value(let val):
                    displayValue = val
                case .Error(let err):
                    display.text = err
                }
            } else {
                displayValue = 0
            }
            updateHistoryLabel()
        }
    }
    
    @IBAction func negate(sender: UIButton) {
        if(userIsTyping) {
            if display.text?.rangeOfString("-") == nil {
                var displayText: String = ["-"]+display.text!
                display.text = displayText
            }
        } else {
            if let operation = sender.currentTitle {
                if let result = brain.performOperation(operation) {
                    switch result {
                        
                    case .Value(let val):
                        displayValue = val
                    case .Error(let err):
                        display.text = err
                    }                } else {
                    displayValue = 0
                }
            }
            updateHistoryLabel()
        }
    }
    
    
    @IBAction func operate(sender: UIButton) {
        if(userIsTyping) {
            enter()
        }
        if let operation = sender.currentTitle {
            if let result = brain.performOperation(operation) {
                switch result {
                case .Value(let val):
                    displayValue = val
                case .Error(let err):
                    display.text = err
                }            } else {
                displayValue = 0
            }
        }
        updateHistoryLabel()
    }
    
    override func viewDidLoad() {
        historyLabel.text = ""
    }
    
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // identify the nav controller embedded in
        var destination = segue.destinationViewController as? UIViewController
        if let navCon = destination as? UINavigationController {
            destination = navCon.visibleViewController
        }
        
        if let gvc = destination as? GraphViewController {
            if let identifier = segue.identifier {
                switch identifier {
                case "graphXY"  : gvc.programFromCalc = brain.program
                default         : gvc.programFromCalc = nil
                }
            }
        }
    }
}

