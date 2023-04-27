import json
import urllib3
import requests
import pytest
import datetime
from colorama import Fore
from requests_kerberos import HTTPKerberosAuth, OPTIONAL

class Test_FreeveeBugAudit():

    @pytest.fixture
    def Web_data_booting(self):
        url = "https://maxis-service-prod-pdx.amazon.com/issues?q=requester:(mohnrsa%20OR%20zuqph%20OR%20deparz%20OR%20vvasante%20OR%20kmaryyu%20OR%20rsumthr%20OR%20srvpn%20OR%20smnandh%20OR%20klsathis%20OR%20hdavisvi)%20AND%20createDate:[NOW-1DAYS%20TO%20NOW]"
        urllib3.disable_warnings()
        SkipAuth = HTTPKerberosAuth(mutual_authentication= OPTIONAL)
        Freevee_Bugs = requests.get(url, auth=SkipAuth, verify=False).text
        self.Freevee_Bugs_Repo = json.loads(Freevee_Bugs)
        self.Bugs_Data = self.Freevee_Bugs_Repo['documents']
        yield
        print('Thank You')

    def test_Defect_Count(self, Web_data_booting):
        Total_Bugs = len(self.Freevee_Bugs_Repo['documents'])
        print ('No. of Bugs/Defects Raised:', Total_Bugs)
        Today = ((str(datetime.datetime.now())).split(' ')[0])
        print (Fore.LIGHTGREEN_EX + 'Date:', Today)
        print ('*' * 30)

        FTV = 0
        Linear = 0
        Roku = 0

        for Individual_Bug in self.Bugs_Data:
            Bugs_Tags = Individual_Bug['tags']
            Individual_Tag_List = [tg['id'] for tg in Bugs_Tags]
            
            for x in Individual_Tag_List:
                if x == "FTV":
                    Component = "FTV"
                    FTV += 1
                elif x == "Roku":
                    Component = "Roku"
                    Roku += 1
                elif x == "Linear channel":
                    Component = "Linear channel"
                    Linear += 1
            print ('Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0])
            
        print ('*' * 30)
        print ('No. Of FTV Bugs:', FTV)
        print ('No. Of Roku Bugs:', Roku)
        print ('No. Of Linear Bugs:', Linear)
        print ('*' * 30)

    def test_Title_Audit(self, Web_data_booting):
        Result = []
        for Individual_Bug in self.Bugs_Data:
            Bug_Titles = Individual_Bug['title']
            print ('Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], Bug_Titles)
            #print (Bug_Titles)
            if len(Bug_Titles) > 30:
                Result.append(True)
                continue
            else:
                print ('~' * 15)
                print (Fore.LIGHTRED_EX + 'Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'Has some Tile Issues')
                print ('~' * 15)
                Result.append(False)
        print ('~' * 15)
        print('Bug Tile Audit Complete')
        print ('*' * 30)
        print ('*' * 30)
        assert False not in Result

    def test_TagCount_Audit(self, Web_data_booting):
        Result = []
        for Individual_Bug in self.Bugs_Data:
            Bugs_Tags = Individual_Bug['tags']
            Individual_Tag_List = [tg['id'] for tg in Bugs_Tags]
            if len(Individual_Tag_List) == 4:
                Result.append(True)
                continue
            elif len(Individual_Tag_List) == 5:
                Result.append(True)
                continue
            else:
                print(Fore.LIGHTRED_EX + 'Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'has Tag Count Mismatch')
                Result.append(False)
        print ('~' * 15)
        print('Tags Count Audit Complete')
        print ('*' * 30)
        print ('*' * 30)
        assert False not in Result

    def test_Tag_Audit(self, Web_data_booting):
        Result = []
        for Individual_Bug in self.Bugs_Data:
            Bugs_Tags = Individual_Bug['tags']
            Individual_Tag_List = [tg['id'] for tg in Bugs_Tags]
            Tags_Attached = []
            Eligible_Tags = ['FTV','Roku','Linear channel','GDQ_QS_Detected_IMDb TV','QS_Adhoc','QS_Testcase','QS-Regression','QS-New feature','QS_Accessibility']
            for x in Individual_Tag_List:
                if x in Eligible_Tags:
                    Tags_Attached.append(x)
                    Result.append(True)
                    continue
                else:
                    print(Fore.LIGHTRED_EX + 'Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'does not contain Proper Tag', x)
                    #print ('~' * 15)
                    Result.append(False)
            #print('Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'has', Tags_Attached, 'Tags')
        print ('~' * 15)
        print('Tag Audit Complete')
        print ('*' * 30)
        print ('*' * 30)
        assert False not in Result

    def test_Assignee_Audit(self, Web_data_booting):
        Result = []
        for Individual_Bug in self.Bugs_Data:
            try:
                Assignee = ((Individual_Bug['assigneeIdentity']).split(':')[1]).split('@')[0]
                Eligible_Assignee = ['spogili','dmallela','katankur', 'phlltr', 'ramadps']    # Data Req
                if Assignee in Eligible_Assignee:
                    Result.append(True)
                    continue
                else:
                    print(Fore.LIGHTRED_EX + 'Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'does not contain proper Assignee i.e', Assignee)
                    #print ('~' * 15)
                    Result.append(False)
            except:
                print(Fore.LIGHTRED_EX + 'Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'does not contain Assignee')
                Result.append(False)
            #print('Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'Assigneed to', Assignee)  
        print ('~' * 15)
        print('Assignee Audit Complete')
        print ('*' * 30)
        print ('*' * 30)
        assert False not in Result

    def test_WatchersCount_Audit(self, Web_data_booting):
        for Individual_Bug in self.Bugs_Data:
            Watchers_List = len(Individual_Bug['watchers'])
            print ('Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'Contains', Watchers_List, 'Watchers')
        print ('~' * 15)
        print('Watchers Count Fetched')
        print ('*' * 30)
        print ('*' * 30)

    def test_Attachment_Audit(self, Web_data_booting):
        Result = []
        for Individual_Bug in self.Bugs_Data:
            Attachment = len(Individual_Bug['attachments'])
            print ('Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'has', Attachment, 'Attachments')
            if Attachment >= 1:
                Result.append(True)
                continue
            else:
                print (Fore.LIGHTRED_EX + 'Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'is not having Attachment')
                Result.append(False)
        print ('~' * 15)
        print('Attachment Audit Complete')
        print ('*' * 30)
        print ('*' * 30)
        assert False not in Result

    def test_Folder_Audit(self, Web_data_booting):
        Result = []
        for Individual_Bug in self.Bugs_Data:
            Bug_Folder = Individual_Bug['assignedFolder']
            Eligible_Folder = ['3b60cad9-3b20-4193-bfda-178890b6ed5d', 'bccb6e93-d499-482b-ba39-7f58b8c31474', '16dc9a7a-ed90-4dad-b589-267786e629c4', '515ddf79-5335-4a26-b19a-ab555b9df6e9', '6cdafd96-a3d4-4e1d-84f5-4fe459710edf']
            if Bug_Folder in Eligible_Folder:
                Result.append(True)
                continue
            else:
                print (Fore.LIGHTRED_EX + 'Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'has Bug Folder Mismatch')
                Result.append(False)
        print ('~' * 15)
        print('Bug Folder Audit Complete')
        print ('*' * 30)
        print ('*' * 30)
        assert False not in Result

    def test_TitleNotation_Audit(self, Web_data_booting):
        Result = []
        for Individual_Bug in self.Bugs_Data:
            Bug_Folder = Individual_Bug['assignedFolder']
            Bug_Titles = Individual_Bug['title']
            if Bug_Folder == ('16dc9a7a-ed90-4dad-b589-267786e629c4'):
                Roku_Title = Bug_Titles.split(']')[0]
                if ('[Roku') in Roku_Title:
                    Result.append(True)
                    continue
                else:
                    Result.append(False)
                    print (Fore.LIGHTRED_EX + 'Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'has Tile Notation Issue', Roku_Title)
            if Bug_Folder == ('3b60cad9-3b20-4193-bfda-178890b6ed5d'):
                FTV_Title = Bug_Titles.split(']')[0]
                if ('[April Rel') in FTV_Title or ('[April Release') in FTV_Title:
                    Result.append(True)
                    continue
                else:
                    Result.append(False)
                    print (Fore.LIGHTRED_EX + 'Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'has Tile Notation Issue', FTV_Title)
            if Bug_Folder == ('bccb6e93-d499-482b-ba39-7f58b8c31474'):
                Linear_Title = Bug_Titles.split(']')[0]
                if ('[Linear channel') in Linear_Title:
                    Result.append(True)
                    continue
                else:
                    Result.append(False)
                    print (Fore.LIGHTRED_EX + 'Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'has Tile Notation Issue' , Linear_Title)
            if Bug_Folder == ('515ddf79-5335-4a26-b19a-ab555b9df6e9'):
                IVA_Title = Bug_Titles.split(']')[0]
                if ('[IVA QS') in IVA_Title:
                    Result.append(True)
                    continue
                else:
                    Result.append(False)
                    print (Fore.LIGHTRED_EX + 'Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'has Tile Notation Issue', IVA_Title)
        print ('~' * 15)
        print('Tilte Notation Audit Complete')
        print ('*' * 30)
        print ('*' * 30)
        assert False not in Result

    def test_TCLinkField_Audit(self, Web_data_booting):
        FResult = []
        for Individual_Bug in self.Bugs_Data:
            Bug_Description = (Individual_Bug['description']).split('\n')
            Bugs_Tags = Individual_Bug['tags']
            Individual_Tag_List = [tg['id'] for tg in Bugs_Tags]
            for x in Individual_Tag_List:
                Result = []
                if x == 'QS_Testcase':
                    for i in Bug_Description:
                        if ((('Test Case Link:') in i or ('TC Link:') in i) or (('Test Case Link :') in i or ('TC Link :') in i) or (('Test Case:') in i or ('Testcase') in i) or (('Test case:') in i or ('Tc Link') in i)):
                            Result.append(True)
                            #print (Fore.LIGHTRED_EX + 'Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'has Test Case Link field')
                            break
                        else:
                            Result.append(False)
                    #print(Result)
                    if True in Result:
                        FResult.append(True)
                    else:
                        FResult.append(False)
                        print (Fore.LIGHTRED_EX + 'Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'Test Case Link field Missing')
        #print(FResult)
        print ('~' * 15)
        print('TC Link field Audit Complete')
        print ('*' * 30)
        print ('*' * 30)
        assert False not in FResult

    def test_FolderTag_Audit(self, Web_data_booting):
        Result = []
        for Individual_Bug in self.Bugs_Data:
            Bug_Folder = Individual_Bug['assignedFolder']
            Bugs_Tags = Individual_Bug['tags']
            Individual_Tag_List = [tg['id'] for tg in Bugs_Tags]
            if Bug_Folder == ('3b60cad9-3b20-4193-bfda-178890b6ed5d'):
                TagList = []
                for i in Individual_Tag_List:
                    TagList.append(i)
                if 'FTV' in TagList:
                    Result.append(True)
                    continue
                else:
                    Result.append(False)
                    print (Fore.LIGHTRED_EX + 'Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'Folder & Tag mismatch')
            if Bug_Folder == ('bccb6e93-d499-482b-ba39-7f58b8c31474'):
                TagList = []
                for i in Individual_Tag_List:
                    TagList.append(i)
                if 'Linear channel' in TagList:
                    Result.append(True)
                    continue
                else:
                    Result.append(False)
                    print (Fore.LIGHTRED_EX + 'Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'Folder & Tag mismatch')
            if Bug_Folder == ('6cdafd96-a3d4-4e1d-84f5-4fe459710edf'):
                TagList = []
                for i in Individual_Tag_List:
                    TagList.append(i)
                if 'Roku' in TagList:
                    Result.append(True)
                    continue
                else:
                    Result.append(False)
                    print (Fore.LIGHTRED_EX + 'Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'Folder & Tag mismatch')
        print ('~' * 15)
        print('Folder & Tag Audit Complete')
        print ('*' * 30)
        print ('*' * 30)
        assert False not in Result

    def test_Regression_Audit(self, Web_data_booting):
        Result = []
        for Individual_Bug in self.Bugs_Data:
            Bug_Folder = Individual_Bug['assignedFolder']
            Bug_Description = (Individual_Bug['description']).split('\n')
            PriResult = []
            if Bug_Folder == ('3b60cad9-3b20-4193-bfda-178890b6ed5d'):
                if ((('Is Regression ? Yes') in Bug_Description or ('Is Regression? Yes') in Bug_Description) or (('Is Regression ? yes') in Bug_Description or ('Is Regression? yes') in Bug_Description)):
                    for i in Bug_Description:
                        if ('Issue is not seen') in i:
                            PriResult.append(True)
                        else:
                            PriResult.append(False)
                    if True in PriResult:
                        Result.append(True)
                        #print ('Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'has Correct Regression Data')
                    else:
                        Result.append(False)
                        print ('Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'has Regression Yes/No Issue')
                elif ((('Is Regression ? No') in Bug_Description or ('Is Regression? No') in Bug_Description) or (('Is Regression ? no') in Bug_Description or ('Is Regression? no') in Bug_Description)):
                    for i in Bug_Description:
                        if ('Issue is also seen') in i:
                            PriResult.append(True)
                        else:
                            PriResult.append(False)
                    if True in PriResult:
                        Result.append(True)
                        #print ('Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'has Correct Regression Data')
                    else:
                        Result.append(False)
                        print ('Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'has Regression Yes/No Issue')
                elif ((('Is Regression ? NA') in Bug_Description or ('Is Regression? NA') in Bug_Description) or (('Is Regression ? NA (New Feature)') in Bug_Description or ('Is Regression? NA(New Feature)') in Bug_Description)):
                    for i in Bug_Description:
                        if ('Issue is also seen') not in i:
                            PriResult.append(True)
                        else:
                            PriResult.append(False)
                    if False not in PriResult:
                        Result.append(True)
                        #print ('Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'has Correct Regression Data')
                    else:
                        Result.append(False)
                        print ('Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'has Regression Yes/No Issue')
        print ('~' * 15)
        print('Regression Yes/No Audit Complete')
        print ('*' * 30)
        print ('*' * 30)
        assert False not in Result

    def test_Severity_Audit(self, Web_data_booting):
        Result = []
        for Individual_Bug in self.Bugs_Data:
            Bug_Folder = Individual_Bug['assignedFolder']
            Impact = Individual_Bug['extensions']['tt']["impact"]
            if Bug_Folder == ('3b60cad9-3b20-4193-bfda-178890b6ed5d'):
                if Impact == 5:
                    Result.append(True)
                    #print ('Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'FTV Bug Raised with severity', Impact)
                else:
                    Result.append(False)
                    print ('Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'FTV Bug Raised with different Severity', Impact)
            if Bug_Folder == ('16dc9a7a-ed90-4dad-b589-267786e629c4'):
                if Impact == 5:
                    Result.append(True)
                    #print ('Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'FTV Bug Raised with severity', Impact)
                else:
                    Result.append(False)
                    print ('Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'FTV Bug Raised with different Severity', Impact)
            if Bug_Folder == ('bccb6e93-d499-482b-ba39-7f58b8c31474'):
                if Impact == 5 or 4:
                    Result.append(True)
                    #print ('Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'FTV Bug Raised with severity', Impact)
                else:
                    Result.append(False)
                    print ('Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'FTV Bug Raised with different Severity', Impact)
        print ('~' * 15)
        print('Severity Audit Complete')
        print ('*' * 30)
        print ('*' * 30)
        assert False not in Result

    def test_TCLink_StatusCode_Audit(self, Web_data_booting):
        TC_Links = []
        Result = []
        for Individual_Bug in self.Bugs_Data:
            Bug_Description = (Individual_Bug['description']).split('\n')
            Bugs_Tags = Individual_Bug['tags']
            Individual_Tag_List = [tg['id'] for tg in Bugs_Tags]
            for x in Individual_Tag_List:
                if x == 'QS_Testcase':
                    for i in Bug_Description:
                        if (((('TC Link:') in i or ('TestCase:') in i)) or (('TC:') in i or ('Test Case:') in i)):
                            Link = i.split(':')[2]
                            TC_Links.append(Link)
        #print(TC_Links)
        for i in TC_Links:
            Response = requests.get('https:' + i)
            if Response.status_code == 200:
                Result.append(True)
            else:
                Result.append(False)
                print ('Test Case Link is not Accesscible', 'https:' + i)
        print ('~' * 15)
        print('Test Case Accesscibility Audit Complete')
        print ('*' * 30)
        print ('*' * 30)
        assert False not in Result

    def test_AccessibilityTitle_Tag_Audit(self, Web_data_booting):
        Result = []
        for Individual_Bug in self.Bugs_Data:
            Bugs_Tags = Individual_Bug['tags']
            Individual_Tag_List = [tg['id'] for tg in Bugs_Tags]
            Bug_Titles = Individual_Bug['title']
            if (('Screen Reader') in Bug_Titles or ('Voice View') in Bug_Titles) or (('Screen reader') in Bug_Titles or ('VV') in Bug_Titles) or (('Voice view') in Bug_Titles or ('Screen Magnification') in Bug_Titles) or (('screen magnification') in Bug_Titles or ('Screen magnification') in Bug_Titles) or (('Screen Magnifier') in Bug_Titles or ('Screen magnifier') in Bug_Titles):
                print (Bug_Titles)
                AvailableTags = []
                for i in Individual_Tag_List:
                    AvailableTags.append(i)
                #print(AvailableTags)
                if 'QS_Accessibility' in AvailableTags:
                    Result.append(True)
                else:
                    print ('Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'does not contain Accessibility Tag')
                    Result.append(False)
        print ('~' * 15)
        print('Test Case Accessibility Bug Tag Audit Complete')
        print ('*' * 30)
        print ('*' * 30)
        assert False not in Result

    def test_Adhoc_TCLinkField_Audit(self, Web_data_booting):
        FResult = []
        for Individual_Bug in self.Bugs_Data:
            Bug_Description = (Individual_Bug['description']).split('\n')
            Bugs_Tags = Individual_Bug['tags']
            Individual_Tag_List = [tg['id'] for tg in Bugs_Tags]
            for x in Individual_Tag_List:
                Result = []
                if x == 'QS_Adhoc':
                    for i in Bug_Description:
                        if ((('Test Case Link:') not in i or ('TC Link:') not in i) or (('Test Case Link :') not in i or ('TC Link :') not in i) or (('Test Case:') not in i)):
                            Result.append(True)
                            #print (Fore.LIGHTRED_EX + 'Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'has Test Case Link field')
                        else:
                            Result.append(False)
                            break
                    #print(Result)
                    if False in Result:
                        FResult.append(False)
                        print (Fore.LIGHTRED_EX + 'Bug ID', Individual_Bug['aliases'][0]["id"], 'raised by', ((Individual_Bug['submitterIdentity']).split(':')[1]).split('@')[0], 'Adhoc Bug contains Test Case Link field')
                    else:
                        FResult.append(True)
        print ('~' * 15)
        print('Adhoc TC Link field Audit Complete')
        print ('*' * 30)
        print ('*' * 30)
        assert False not in Result
