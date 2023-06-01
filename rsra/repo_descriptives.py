from sickle import Sickle


#url: str = field(default='', metadata={'description': 'OAI URL'}) # Sickle
#core_id: str = field(default='', metadata={'description': 'CORE Identifier'}) 
#open_doar_id: str = field(default='', metadata={'description': 'Open DOAR identifier'})
#name: str = field(default='', metadata={'description': 'Name of repository'}) # Sickle
#russell_member: str = field(default='', metadata={'description': 'If the university is a member of the Russell Group of research intensive universities'})
#rse_group: str = field(default='', metadata={'description': 'If an RSE group is present (based on Soc of RSE data)'})
#email: str = field(default='', metadata={'description': 'Redacted'}) # Sickle
#uri: str = field(default='', metadata={'description': 'Not used'})
#uni_sld: str = field(default='', metadata={'description': 'Second level domain (the part of the url between . And .ac.uk. Used to identify multiple repositories from the same institute.'})
#home_page_url: str = field(default='', metadata={'description': 'Main University website'}) # Sickle
#source: str = field(default='', metadata={'description': 'Not used'})
#ris_software: str = field(default='', metadata={'description': 'the Research Information System software used'})
#ris_software_enum: Enum = field(default=ris_enum.OTHER, metadata={'description': 'Resolve ris_software into similar types (e.g. Eprints 3, EPrints3.3.16 both equal eprints)'})
#metadata_format: str = field(default='', metadata={'description': 'format of metadata protocol e.g. DC, OAI_DC, RIOXX'})
#created_date: str = field(default='', metadata={'description': 'Repository creation date'}) # Sickle
#location: dict = field(default='', metadata={'description': 'Lat and long of institute'}) 
#logo: str = field(default='', metadata={'description': 'Not used'})
#provider_type: str = field(default='repository', metadata={'description': 'Type of data source e.g. repository, journal etc.  Always Repository for this data set.'})
#stats: str = field(default='', metadata={'description': 'Not used'})
#contains_software_set: str = field(default='', metadata={'description': 'Whether the OAI-PMH software set is present in the repository.'})
#num_software_records: str = field(default='', metadata={'description': 'The response of the OAI-PMH query for software (erroneous as discussed in paper)'})
#error: str = field(default='', metadata={'description': 'The category of error returned by the experiment’s OAI-PMH queries (see paper)'})
#manual_num_software_records: str = field(default='', metadata={'description': 'The true amount of software contained in the repository as found by a manual exhaustive search of each university website'})
#category: str = field(default='', metadata={'description': 'Whether the repository (a) contains software; (b) can contain software, but doesn’t yet; (c) has no separate type of research output called software or similar'})
#search_query: str = field(default='', metadata={'description': 'the search query used to replicate the search within a browser.'})


def get_oai_from_ris_type(url):

    #PURE = ws/oai

    #dspace = /oai/request
    #dspace-oai/request
    print(url)




def get_repo_descriptives(oai_url: str):

    sickle = Sickle(oai_url)

    identity = sickle.Identify()
    print(identity._identify_dict)

    print(identity.repositoryName)
    print(identity.baseURL)
    print(identity.protocolVersion)
    print(identity.adminEmail)
    print(identity.earliestDatestamp)
    print(identity.deletedRecord)
    print(identity.granularity)
    print(identity.description)
    print(identity.oai_identifier)
    print(identity.scheme)
    print(identity.repositoryIdentifier)
    print(identity.delimiter)
    print(identity.sampleIdentifier)


get_repo_descriptives('https://ora.ox.ac.uk/oai2/')
