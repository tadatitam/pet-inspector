import sys                                          # exit
sys.path.insert(0, "..")                            # to import files from parent directory
import common.data_interface as di                  # data_interface
import common.texify as texify                      # for texifying results


fmap = {     # fprint -> fpData name
    "h.User-Agent":"userAgentHttp",
    "h.Accept":"acceptHttp",
    "h.Accept-Encoding":"encodingHttp",
    "h.Accept-Language":"languageHttp",
    "plugins":"pluginsJS",
    "platform":"platformJS",
    "cookies enabled":"cookiesJS",
    "DNT enabled":"dntJS",
    "timezone":"timezoneJS",
#         "screen.AvailHeight":"screenHeight",
#         "screen.AvailWidth": "screenWidth",
    "screen.Width": "screenWidth",
    "screen.Height":"screenHeight",
    "screen.Depth":"screenDepth",
    "local storage":"localJS",
    "session storage":"sessionJS",
    "IE addBehavior":"IEDataJS",
    "adBlock installed":"adBlock",
    "webGL.Vendor":"vendorWebGLJS",
    "webGL.Renderer":"rendererWebGLJS",
#     "canvas fingerprint":"canvasJSHashed",
#     "webGL.Data Hash":"webGLJs"
}

if __name__ == "__main__":
    query = '''SELECT * FROM fpData WHERE NOT (id='Not Supported')''' #  OR userAgentHttp LIKE '%20100101%'
    tuples = di.get_data(query)
    print "total tuples", len(tuples)
    user_tuples = di.per_user(tuples)
    print "unique cookie tuples", len(user_tuples)
    user_tuples = di.sanitize(user_tuples)
    print "sanitized", len(user_tuples)
    
    attributes_to_check = {
            'h.User-Agent': 
                ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36', 
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0', 
                'Mozilla/5.0 (X11; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0'], 
#                 ['Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0',
#                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0',
#                 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
#                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
#                 ],
            'h.Accept-Language':
                ['ja,en-US;q=0.9,en;q=0.8', 
                'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 
                'en-US,en;q=0.9', 
                'ar,en-US;q=0.9,en;q=0.8', 
                'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7', 
                'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7', 
                'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
                'ja,en-US;q=0.7,en;q=0.3', 
                'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3', 
                'de,en-US;q=0.7,en;q=0.3', 
                'en-US,en;q=0.5', 
                'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3', 
                'ar,en-US;q=0.7,en;q=0.3', 
                'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3'], 
            'platform':
                ['MacIntel', 'Linux x86_64'],
            'screen.Height':
#                 ['1080', '768', '900'],
                ['256', '900', '550', '200', '2000', '721', '3000'], 
            'screen.Width':
#                 ['1920', '1440', '1024'],
                ['320', '6000', '450', '300', '2000', '850', '1440'], 
            'screen.Depth':
                ['24', '16', '8'], 
            'timezone':
#                 ['420', '360', '-360'],
                ['480', '360', '-660', '-180', '180', '-360', '660'], 
            'webGL.Renderer':                
#                 ['Google SwiftShader', 
#                 'NVIDIA GeForce GT 650M OpenGL Engine',
#                 'Gallium 0.4 on llvmpipe (LLVM 4.0, 256 bits)', 
#                 'Gallium 0.4 on llvmpipe (LLVM 3.4, 256 bits)'
#                 ],
                ['Google SwiftShader', 
                'NVIDIA GeForce GT 650M OpenGL Engine',
                'Not supported', 
                'Gallium 0.4 on llvmpipe (LLVM 3.4, 256 bits)', 
                'llvmpipe (LLVM 5.0, 256 bits)', 
                'Gallium 0.4 on llvmpipe (LLVM 3.5, 256 bits)'], 
            'webGL.Vendor':
                ['Google Inc.', 
                'NVIDIA Corporation', 
                'VMware, Inc.', 
                'Not supported']
#             'resolutionJS':
#                 ['1920x1080x24', '1440x900x24', '1024x768x24']
        }
        
    texify.base_surprisal_original(user_tuples, attributes_to_check, fmap, filename = "orgbase.tex")
    texify.base_surprisal_alternate(user_tuples, attributes_to_check, fmap, filename = "altbase.tex")
    



