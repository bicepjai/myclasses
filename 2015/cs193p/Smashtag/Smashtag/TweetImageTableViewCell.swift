//
//  TweetImageTableViewCell.swift
//  Smashtag
//
//  Created by Jayaram Prabhu Durairaj on 3/18/15.
//  Copyright (c) 2015 bicepjai. All rights reserved.
//

import UIKit

class TweetImageTableViewCell: UITableViewCell {

    var imageURL: NSURL? {
        didSet {
            cellImage = nil
            fetchImage()
        }
    }
    
    func viewForZoomingInScrollView(scrollView: UIScrollView) -> UIView? {
        return imageView
    }
    
    @IBOutlet weak var scrollView: UIScrollView!{
        didSet {
            scrollView.contentSize = cellImageView.frame.size
            scrollView.minimumZoomScale = 0.03
            scrollView.maximumZoomScale = 1.0
            scrollView.zoomScale = 1.0;
            
        }
    }
    
    @IBOutlet weak var spinner: UIActivityIndicatorView!
    
    private func fetchImage() {
        if let url = imageURL {
            spinner?.startAnimating()
            let qos = Int(QOS_CLASS_USER_INITIATED.value)
            dispatch_async(dispatch_get_global_queue(qos, 0)) {
                () -> Void in
                let imageData = NSData(contentsOfURL: url)
                dispatch_async(dispatch_get_main_queue()) {
                    if url == self.imageURL {
                        if imageData != nil {
                            self.cellImage = UIImage(data: imageData!)
                        } else {
                            self.cellImage = nil
                        }
                    }
                }
            }
        }
    }
    
    private var cellImageView = UIImageView()
    
    private var cellImage: UIImage? {
        get { return cellImageView.image }
        set {
            cellImageView.image = newValue
            cellImageView.sizeToFit()
            scrollView?.contentSize = cellImageView.frame.size
            spinner?.stopAnimating()
        }
    }
    
}
