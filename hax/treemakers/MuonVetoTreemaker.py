class MuonVetoTreemaker(hax.minitrees.TreeMaker):
    """Computing properties of the Muon Veto Events
    
    This TreeMaker will ignore all TPC related events which are stored as objects of PAX classes like 'peaks' or 'interactions'.
    It gets the information of the MV events from the array stored in events.all_hits as numpy dtype array similar to objects
    from the PAX 'Hit' class.
    
    Versioning:
    V0.0.1 - 2016/10/07 - ChG: Kick-Off
    V1.0.0 - 2016/10/13 - ChG: First working version. Possible to get
    all events of the file and successful comparison what one can see
    in a ROOT TBrowser
    V1.0.1 - 2016/10/19 - ChG: Added 'Hit_width' in computations
    V1.1.0 - 2016/10/20 - ChG: Accepts now datasets with empty first
    event entry (error before)
    V1.1.1 - 2017/02/15 - ChG: Added 'Hit_noise_sigma' for calculation
    of threshold for each hit
    """
    
    extra_branches = ['*']  # Activate all of ROOT file
    __version__ = '1.1.1'
    uses_arrays = True
    
    def extract_data(self, event):  # This runs on each event
        
        # Create default dictionary
        #values = defaultdict(list)
        values ={}
        
        values['PMTs'] = []                       # PMT Channel which got hit in the event
        values['Hit_area'] = []                   # Area of signal in each PMT Channel [PE] really PE?
        values['Hit_height'] = []                 # Height of signal in each PMT Channel [PE/samples]
        values['Hit_left'] = []                   # left boundary of signal in each PMT Channel [samples after eventstart]
        values['Hit_center'] = []                 # Center of signal in each PMT Channel [ns] 1 ns = 0.1 samples
        values['Hit_right'] = []                  # right boundary of signal in each PMT Channel [samples after eventstart]
        values['Hit_width'] = []                  # peak width of each PMT Channel [samples]
        values['Hit_noise_sigma'] = []            # Noise sigma of the pulse in which the hit was found [pe/samples]
        #values['NumPMTsHit'] = 0                  # Number of PMT Channels which got hit in the event
        
        # Store start/stop time of event
        values['tStart'] = event.start_time       # Starttime of the event (Unixtime)
        values['tStop'] = event.stop_time         # Stoptime of the event (Unixtime)
        
        # Some events do not have a single hits, whatever that means....if so, do nothing and jump to next event
        if not len(event.all_hits):
            values['PMTs'].append(np.nan)         # necessary to note fail if first event is empty (has no hits)
            values['Hit_area'].append(np.nan)           #  ^
            values['Hit_height'].append(np.nan)         #  |
            values['Hit_left'].append(np.nan)           #  |
            values['Hit_center'].append(np.nan)         #  |
            values['Hit_right'].append(np.nan)          #  |
            values['Hit_width'].append(np.nan)          #  |
            values['Hit_noise_sigma'].append(np.nan)    #  |
            return values
        
        #values['NumPMTsHit'] = len(event.all_hits)
        
        for i in range(len(event.all_hits)):
            values['PMTs'].append(event.all_hits[i].channel)
            values['Hit_area'].append(event.all_hits[i].area)
            values['Hit_height'].append(event.all_hits[i].height)
            values['Hit_left'].append(event.all_hits[i].left)
            values['Hit_center'].append(event.all_hits[i].center)
            values['Hit_right'].append(event.all_hits[i].right)
            values['Hit_width'].append(event.all_hits[i].right - event.all_hits[i].left)
            values['Hit_noise_sigma'].append(event.all_hits[i].noise_sigma)

        return values
