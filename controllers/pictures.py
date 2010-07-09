import os
from lib import controller

class pictures(controller.Controller):

    def index(self):
        crudem_pictures = (
            {'small':'http://crudem.org/images/stories/gallery/incoming-patients/vsig_thumbs/024_90_67_80.jpg',
             'big':'http://crudem.org/images/stories/gallery/incoming-patients/024.jpg'},
            {'small':'http://crudem.org/images/stories/gallery/incoming-patients/vsig_thumbs/041_90_67_80.jpg',
             'big':'http://crudem.org/images/stories/gallery/incoming-patients/041.jpg'},
            {'small':'http://crudem.org/images/stories/gallery/incoming-patients/vsig_thumbs/174_90_67_80.jpg',
             'big':'http://crudem.org/images/stories/gallery/incoming-patients/174.jpg'},
            {'small':'http://crudem.org/images/stories/gallery/incoming-patients/vsig_thumbs/096_90_67_80.jpg',
             'big':'http://crudem.org/images/stories/gallery/incoming-patients/096.jpg'},
            {'small':'http://crudem.org/images/stories/gallery/incoming-patients/vsig_thumbs/039_90_67_80.jpg',
             'big':'http://crudem.org/images/stories/gallery/incoming-patients/039.jpg'},
            {'small':'http://crudem.org/images/stories/gallery/volunteers/vsig_thumbs/Physical_Therapist_90_67_80.jpg',
             'big':'http://crudem.org/images/stories/gallery/volunteers/Physical_Therapist.jpg'},
            {'small':'http://crudem.org/images/stories/gallery/volunteers/vsig_thumbs/at_the_market_90_67_80.jpg',
             'big':'http://crudem.org/images/stories/gallery/volunteers/at_the_market.jpg'},
            {'small':'http://crudem.org/images/stories/gallery/volunteers/vsig_thumbs/Helping_Hands_90_67_80.jpg',
             'big':'http://crudem.org/images/stories/gallery/volunteers/Helping_Hands.jpg'},
            {'small':'http://crudem.org/images/stories/gallery/volunteers/vsig_thumbs/Operating_90_67_80.jpg',
             'big':'http://crudem.org/images/stories/gallery/volunteers/Operating.jpg'},
            {'small':'http://crudem.org/images/stories/gallery/first-response/vsig_thumbs/DSC_0876_90_53_80.jpg',
             'big':'http://crudem.org/images/stories/gallery/first-response/DSC_0876.jpg'}
            )

                    
        return self.render("pictures", crudem_pictures = crudem_pictures)
    
