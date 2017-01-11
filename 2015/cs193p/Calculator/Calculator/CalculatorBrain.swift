//
//  CalculatorBrain.swift
//  calculator
//
//  Created by bicepjai on 2/5/15.
//  Copyright (c) 2015 bicepjai. All rights reserved.
//

import Foundation

class CalculatorBrain
{
    enum Result: Printable
    {
        case Value(Double)
        case Error(String)
        
        var description: String {
            get {
                switch self {
                case .Error(let errString):
                    return ("\(errString)")
                case .Value(let val):
                    return ("\(val)")
                    
                }
            }
        }
    }
    
    private enum Op: Printable
    {
        case Operand(Double)
        case Variable(String)
        case NullaryOperation(String, () -> Double)
        
        case UnaryOperation(String, Double -> Double, (Double -> String?)? )
        case BinaryOperation(String, (Double,Double) -> Double, Int, ((Double, Double) -> String?)?)
        
        var description: String {
            get {
                switch self {
                case .Operand(let operand):
                    return "\(operand)"
                case .Variable(let symbol):
                    return symbol
                case .UnaryOperation(let symbol, _, _):
                    return symbol
                case .NullaryOperation(let symbol, _):
                    return symbol
                case .BinaryOperation(let symbol, _, _, _):
                    return symbol
                }
            }
        }
        
        var opPrec: Int {
            get {
                switch self {
                    case .BinaryOperation(_, _, let prec, _):
                        return prec
                    default:
                        return Int.max
                }
            }
        }
    }
    
    private var opStack = [Op]()
    private var knownOps = [String:Op]()
    
    var variableValues = [String:Double]()
    var description: String! {
        get {
            var remainder = opStack
            var result = ""
            while !remainder.isEmpty {
                let desc = describe(remainder)
                let output = desc.result ?? "?"
                result = " " + output + "," + result
                remainder = desc.remainingOps
            }
            if result == "" {
                return " "
            }
            return dropFirst(dropLast(result))
        }
    }
    
    private func describe(ops: [Op]) -> (result: String?, prec: Int?, remainingOps: [Op]) {
        if !ops.isEmpty {
            var remainingOps = ops
            let op = remainingOps.removeLast()
            let prec = op.opPrec
            let opDesc = op.description
            switch op {
            case .UnaryOperation:
                let op1Desc = describe(remainingOps)
                let operand1 = op1Desc.result ?? "?"
                return (opDesc + "(" + operand1 + ")", prec, op1Desc.remainingOps)
            case .BinaryOperation:
                let op1Desc = describe(remainingOps)
                var operand1 = op1Desc.result ?? "?"
                let prec1 = op1Desc.prec ?? Int.max
                if prec1 < prec {
                    operand1 = "(" + operand1 + ")"
                }
                let op2Desc = describe(op1Desc.remainingOps)
                var operand2 = op2Desc.result ?? "?"
                let prec2 = op2Desc.prec ?? Int.max
                if prec2 < prec {
                    operand2 = "(" + operand2 + ")"
                }
                return (operand2 + opDesc + operand1, prec, op2Desc.remainingOps)
            default:
                return (opDesc, prec, remainingOps)
            }
        }
        return (nil, nil, ops)
    }
    
    init() {
        func learnOp (op : Op) {
            knownOps[op.description] = op
        }
        
        learnOp(Op.BinaryOperation("÷",     {$1 / $0},  1, {
            op0, op1 in
            if op0 == 0.0 {
                return "Err: Div by Zero"
            }
            return nil
        }))
        
        learnOp(Op.BinaryOperation("×",     *,          2, nil))
        learnOp(Op.BinaryOperation("+",     +,          3, nil))
        learnOp(Op.BinaryOperation("−",     {$1 - $0},  4, nil))
        
        learnOp(Op.UnaryOperation("√",      sqrt,       {
            op1 in
            if op1 < 0 {
                return "Err: Sqrt of -ve"
            }
            return nil
        }))
        
        learnOp(Op.UnaryOperation("cos",    cos,        nil))
        learnOp(Op.UnaryOperation("sin",    sin,        nil))
        learnOp(Op.NullaryOperation("∏",    {M_PI}))
        learnOp(Op.UnaryOperation("±",      {-$0},      nil))
    }
    
    func pushOperand(operand: Double) -> Result? {
        opStack.append(Op.Operand(operand))
        return evaluate()
    }
    
    func pushOperand(symbol: String) -> Result? {
        opStack.append(Op.Variable(symbol))
        return evaluate()
    }
    
    func undo() -> Result? {
        opStack.removeLast()
        return evaluate()
    }
    
    func performOperation(symbol: String) -> Result? {
        if  let operation = knownOps[symbol] {
            opStack.append(operation)
        }
        return evaluate()
    }
    
    typealias PropertyList = AnyObject
    var program: AnyObject { // gauranteed to be PropertyList
        get {
            return opStack.map{ $0.description }
        }
        set {
            if let opSymbols = newValue as? Array<String> {
                var newOpStack = [Op]()
                for opSymbol in opSymbols {
                    if let op = knownOps[opSymbol] {
                        newOpStack.append(op)
                    } else if let operand = NSNumberFormatter().numberFromString(opSymbol)?.doubleValue {
                        newOpStack.append(.Operand(operand))
                    } else {
                        newOpStack.append(.Variable(opSymbol))
                    }
                }
                opStack = newOpStack
            }
        }
    }
   
    func getMemory (key: String?) -> Double? {
        if key != nil {
            return variableValues[key!]
        }
        return nil
    }
    
    func setMemory (key: String?, mem: Double?) {
        if key != nil && key != nil {
            variableValues[key!] = mem!
        }
    }
    
    private func evaluate(ops: [Op]) -> (result: Result, remainingOps: [Op]) {
        if(!ops.isEmpty) {
            var remainingOps = ops
            let op = remainingOps.removeLast()
            
            switch op {
                case .Operand(let operand):
                    return (.Value(operand), remainingOps)

                case .Variable(let symbol):
                    if let vVal = variableValues[symbol] {
                        return (.Value(vVal), remainingOps)
                    }
                    return(.Error("Err: Variable not set"), remainingOps)

                case .NullaryOperation( _, let operation):
                    return (.Value(operation()), remainingOps)
                    
                case .UnaryOperation( _, let operation, let evalFunc):
                    let op1Evaluation = evaluate(remainingOps)
                    switch op1Evaluation.result {
                        case .Value(let val):
                            if let ef = evalFunc?(val) {
                                return (.Error(ef), op1Evaluation.remainingOps)
                            }
                            return (.Value(operation(val)), op1Evaluation.remainingOps)
                        
                        case .Error(let err):
                            return (.Error(err), op1Evaluation.remainingOps)
                    }
                    
                case .BinaryOperation( _, let operation, _, let evalFunc):
                    let op1Evaluation = evaluate(remainingOps)
                    switch op1Evaluation.result {
                        
                        case .Value(let val1):
                            let op2Evaluation = evaluate(op1Evaluation.remainingOps)
                            switch op2Evaluation.result {
                                
                                case .Value(let val2):
                                    if let ef = evalFunc?(val1, val2) {
                                        return (.Error(ef), op2Evaluation.remainingOps)
                                    }
                                    return (.Value(operation(val1,val2)), op2Evaluation.remainingOps)
                                
                                case .Error(let err):
                                    return (.Error(err), op2Evaluation.remainingOps)
                            }
                        
                        case .Error(let err):
                            return (.Error(err), op1Evaluation.remainingOps)
                    }
            }
        }
        return(.Error("Err: Too Few Ops"), ops)
    }
    
    func evaluate()-> Result? {
        let (result, remainder) = evaluate(opStack)
//        println("\(opStack) = \(result) with \(remainder) left over")
        return result
    }
    
    func clearCalcBrain() {
        opStack.removeAll(keepCapacity: false)
        variableValues.removeAll(keepCapacity: false)
    }
    
}

