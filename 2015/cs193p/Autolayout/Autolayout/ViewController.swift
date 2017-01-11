//
//  ViewController.swift
//  Autolayout
//
//  Created by bicepjai on 2/25/15.
//  Copyright (c) 2015 bicepjai. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    @IBOutlet weak var loginField: UITextField!
    @IBOutlet weak var passwordField: UITextField!
    @IBOutlet weak var passwordLabel: UILabel!
    
    @IBOutlet weak var companyLabel: UILabel!
    @IBOutlet weak var nameLabel: UILabel!
    
    @IBOutlet weak var imageView: UIImageView!
    
    var secure: Bool = false {
        didSet {
            updateUI()
        }
    }
    
    var loggedInUser: User? {
        didSet {
            updateUI()
        }
    }
    
    var image: UIImage? {
        get {
            return imageView.image
        }
        set {
            imageView.image = newValue
            if let constrainedView = imageView {
                if let newImage = newValue {
                    aspectRatioConstraint = NSLayoutConstraint(
                        item: constrainedView,
                        attribute: .Width,
                        relatedBy: .Equal,
                        toItem: constrainedView,
                        attribute: .Height,
                        multiplier: newImage.aspectRatio,
                        constant: 0)
                } else {
                    aspectRatioConstraint = nil
                }
            }
        }
    }
    
    var aspectRatioConstraint: NSLayoutConstraint? {
        willSet {
            if let existingConstraint = aspectRatioConstraint {
                view.removeConstraint(existingConstraint)
            }
        }
        
        didSet {
            if let newConstraint = aspectRatioConstraint {
                view.addConstraint(newConstraint)
            }
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        updateUI()
        
    }
    private func updateUI() {
        passwordField.secureTextEntry = secure
        passwordLabel.text = secure ? "Secure Password" : "Password"
        nameLabel.text = loggedInUser?.name
        companyLabel.text = loggedInUser?.company
        image = loggedInUser?.image
    }
    
    @IBAction func toggleSecurity(sender: UIButton) {
        secure = !secure
    }
    
    @IBAction func login(sender: UIButton) {
        loggedInUser = User.login(loginField.text ?? "", password: passwordField.text ?? "")
    }
    
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

}

extension User {
    var image: UIImage? {
        if let image = UIImage(named: login) {
            return image
        } else {
            return UIImage(named: "unknown_user")
        }
    }
}

extension UIImage {
    var aspectRatio: CGFloat {
        return size.height != 0 ? size.width / size.height : 0
    }
}
