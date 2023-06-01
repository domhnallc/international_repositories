from dataclasses import dataclass, field
from enum import Enum
import json
from dataclasses_json import dataclass_json

class ris_enum(Enum):
  '''Defines the enums for the RIS platforms.  Used to refine all varieties of response into one e.g., EPrints2, Eprints3.3.1.6, EPrints => eprints'''

  EPRINTS = "eprints"
  DSPACE = "dspace"
  PURE = "pure"
  HAPLO = "haplo"
  WORKTRIBE = "worktribe"
  EXLIBRIS = "exlibris"
  FEDORA = "fedora"
  EQUELLA = "equella"
  QAICAT = "qaicat"
  OTHER = "other"

@dataclass_json
@dataclass
class Base_repository:
    """
    _summary_ : Base dataclass to hold all variables for each record of each repository
    _attributes_ :
    url: str 	
        OAI URL
    core_id: str 	
        CORE Identifier
    open_doar_id: str 	
        Open DOAR identifier
    name: str 	
        Name of repository
    russell_member: str 	
        If the university is a member of the Russell Group of research intensive universities
    rse_group: str 	
        If an RSE group is present (based on Soc of RSE data)
    email: str 	
        Redacted
    uri: str 	
        Not used
    uni_sld: str 	
        Second level domain (the part of the url between . And .ac.uk. Used to identify multiple repositories from the same institute.
    home_page_url: str 	
        Main University website
    source: str 	
        Not used
    ris_software: str 	
        the Research Information System software used
    ris_software_enum: Enum 	
        Resolve ris_software into similar types (e.g. Eprints 3, EPrints3.3.16 both equal eprints)
    metadata_format: str 	
        format of metadata protocol e.g. DC, OAI_DC, RIOXX
    created_date: str 	
        Repository creation date
    location: dict 	
        Lat and long of institute 
    logo: str 	
        Not used
    provider_type: str 
        Type of data source e.g. repository, journal etc.  Always Repository for this data set. (default = Repository)
    stats: str 	
        Not used
    contains_software_set: str 	
        Whether the OAI-PMH software set is present in the repository.
    num_software_records: str 	
        The response of the OAI-PMH query for software (erroneous as discussed in paper)
    error: str 	
        The category of error returned by the experiment’s OAI-PMH queries (see paper)
    manual_num_software_records: str 	
        The true amount of software contained in the repository as found by a manual exhaustive search of each university website
    category: str 	
        Whether the repository (a) contains software; (b) can contain software, but doesn’t yet; (c) has no separate type of research output called software or similar

    """   
    url: str = field(default='', metadata={'description': 'OAI URL'}) # Sickle
    core_id: str = field(default='', metadata={'description': 'CORE Identifier'}) 
    open_doar_id: str = field(default='', metadata={'description': 'Open DOAR identifier'})
    name: str = field(default='', metadata={'description': 'Name of repository'}) # Sickle
    russell_member: str = field(default='', metadata={'description': 'If the university is a member of the Russell Group of research intensive universities'})
    rse_group: str = field(default='', metadata={'description': 'If an RSE group is present (based on Soc of RSE data)'})
    email: str = field(default='', metadata={'description': 'Redacted'}) # Sickle
    uri: str = field(default='', metadata={'description': 'Not used'})
    uni_sld: str = field(default='', metadata={'description': 'Second level domain (the part of the url between . And .ac.uk. Used to identify multiple repositories from the same institute.'})
    home_page_url: str = field(default='', metadata={'description': 'Main University website'}) # Sickle
    source: str = field(default='', metadata={'description': 'Not used'})
    ris_software: str = field(default='', metadata={'description': 'the Research Information System software used'})
    ris_software_enum: Enum = field(default=ris_enum.OTHER, metadata={'description': 'Resolve ris_software into similar types (e.g. Eprints 3, EPrints3.3.16 both equal eprints)'})
    metadata_format: str = field(default='', metadata={'description': 'format of metadata protocol e.g. DC, OAI_DC, RIOXX'})
    created_date: str = field(default='', metadata={'description': 'Repository creation date'}) # Sickle
    location: dict = field(default='', metadata={'description': 'Lat and long of institute'}) 
    logo: str = field(default='', metadata={'description': 'Not used'})
    provider_type: str = field(default='repository', metadata={'description': 'Type of data source e.g. repository, journal etc.  Always Repository for this data set.'})
    stats: str = field(default='', metadata={'description': 'Not used'})
    contains_software_set: str = field(default='', metadata={'description': 'Whether the OAI-PMH software set is present in the repository.'})
    num_software_records: str = field(default='', metadata={'description': 'The response of the OAI-PMH query for software (erroneous as discussed in paper)'})
    error: str = field(default='', metadata={'description': 'The category of error returned by the experiment’s OAI-PMH queries (see paper)'})
    manual_num_software_records: str = field(default='', metadata={'description': 'The true amount of software contained in the repository as found by a manual exhaustive search of each university website'})
    category: str = field(default='', metadata={'description': 'Whether the repository (a) contains software; (b) can contain software, but doesn’t yet; (c) has no separate type of research output called software or similar'})
    search_query: str = field(default='', metadata={'description': 'the search query used to replicate the search within a browser.'})

    def convert_to_dict(self) -> json:
        """_summary_

        Returns:
            json: _description_
        """    
        return self.to_dict()
       
    
