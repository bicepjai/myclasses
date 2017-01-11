//
//  GraphView.swift
//  Calculator
//
//  Created by Jayaram Prabhu Durairaj on 3/8/15.
//  Copyright (c) 2015 bicepjai. All rights reserved.
//

import UIKit


protocol GraphViewDataSource: class {
    func yForX(sender: GraphView, x: CGFloat) -> CGFloat?
}

@IBDesignable
class GraphView: UIView {

    func updateDetails() {
        graphDetails["Scale"] = "\(defaults.objectForKey(GraphHistory.ScaleKey) as? CGFloat ?? 1.0)"
        graphDetails["Origin"] = defaults.objectForKey(GraphHistory.OriginKey) as? String
    }

    private struct GraphHistory {
        static let DefaultsKey = "GraphDetails.History"
        static let OriginKey = "GraphView.Origin"
        static let ScaleKey = "GraphView.Scale"
    }
    
    private let defaults = NSUserDefaults.standardUserDefaults()
    
    weak var dataSource: GraphViewDataSource?
    
    @IBInspectable
    var scale: CGFloat {
        get {
            return defaults.objectForKey(GraphHistory.ScaleKey) as? CGFloat ?? 1.0
        }
        set {
            graphDetails["Scale"] = "\(newValue)"
            defaults.setObject(newValue, forKey:GraphHistory.ScaleKey)
            setNeedsDisplay()
        }
    }
    
    @IBInspectable
    var color: UIColor = UIColor.blackColor() {didSet {setNeedsDisplay()}}
    @IBInspectable
    var lineWidth: CGFloat = 1.0 {didSet {setNeedsDisplay()}}
    
    let axesdrawer = AxesDrawer()

    private var axesOrigin: CGPoint? { didSet { setNeedsDisplay() } }
    
    var origin: CGPoint {
        get {
            if let nsudCenter = defaults.objectForKey(GraphHistory.OriginKey) as? String {
                let center = CGPointFromString(nsudCenter)
                return convertPoint(center, fromView: superview)
            }
            return convertPoint(center, fromView: superview)
        }
        set {
            axesOrigin = newValue
            graphDetails["Origin"] = NSStringFromCGPoint(axesOrigin!)
            defaults.setObject(NSStringFromCGPoint(axesOrigin!), forKey:GraphHistory.OriginKey)
        }
    }

    var graphDetails = [String:String]()
    
    override func drawRect(rect: CGRect) {
        axesdrawer.drawAxesInRect(bounds, origin: origin, pointsPerUnit: scale)

        let path = UIBezierPath()
        path.lineWidth = lineWidth
        
        var prevXY:CGPoint!
        var currentXY:CGPoint!
        var point = CGPoint()
        
         for i in 0...Int(bounds.size.width * contentScaleFactor) {
            point.x = CGFloat(i) / contentScaleFactor
            if let y = dataSource?.yForX(self,x: (point.x - origin.x) / contentScaleFactor) {
                if !y.isNormal && !y.isZero {
                    continue
                }
                point.y = origin.y - y * scale
                if prevXY == nil {
                    prevXY = point
                    path.moveToPoint(prevXY)
                } else {
                    currentXY = point
                    path.addLineToPoint(currentXY)
                    path.moveToPoint(currentXY)
                }
            }
        }
        path.stroke()
    }

    private struct Constants {
        static let panAreaRadius: CGFloat = 50.0
    }
    // MARK: - Gesture Actions
    
    func scale(gesture: UIPinchGestureRecognizer) {
        if gesture.state == .Changed {
            scale *= gesture.scale
            gesture.scale = 1
        }
    }
    
    private var canPan: Bool = false
    
    func checkForPan(panStartingPoint: CGPoint) -> Bool {
        let panStartArea = UIBezierPath(
            arcCenter: origin,
            radius: Constants.panAreaRadius,
            startAngle: 0,
            endAngle: CGFloat(2*M_PI),
            clockwise: true
            )
        if panStartArea.containsPoint(panStartingPoint) {
            return true
        } else {
            return false
        }
    }
    
    func moveOrigin(gesture: UIPanGestureRecognizer) {
        switch gesture.state {
            case .Began:
                let location = gesture.locationInView(self)
                if checkForPan(location) {
                    canPan = true
                }
            case .Changed:
                if canPan {
                    origin = gesture.locationInView(self)
                }
            case .Ended: canPan = false
            default: break
        }
    }

    func changeOrigin(gesture: UITapGestureRecognizer) {
        switch gesture.state {
        case .Ended:
            origin = gesture.locationInView(self)
        default: break
        }
    }
    
}
