def check_city_support(city, state):
        if state.lower() == 'texas':
            city_coordinates = {
                    'houston': [29.7604, -95.3698],
                    'san antonio': [29.4241, -98.4936],
                    'dallas': [32.7767, -96.7970],
                    'austin': [30.2672, -97.7431],
                    'fort worth': [32.7555, -97.3308],
                    'el paso': [31.7619, -106.4850],
                    'arlington': [32.7357, -97.1081],
                    'corpus christi': [27.8006, -97.3964],
                    'plano': [33.0198, -96.6989],
                    'laredo': [27.5306, -99.4803],
                    'lubbock': [33.5779, -101.8552],
                    'garland': [32.9126, -96.6389],
                    'irving': [32.8140, -96.9489],
                    'amarillo': [35.2210, -101.8313],
                    'grand prairie': [32.7459, -96.9978],
                    'brownsville': [25.9018, -97.4975],
                    'mckinney': [33.1972, -96.6397],
                    'frisco': [33.1507, -96.8236],
                    'pasadena': [29.6911, -95.2091],
                    'mesquite': [32.7668, -96.5992],
                    'killeen': [31.1171, -97.7278],
                    'mcallen': [26.2034, -98.2300],
                    'carrollton': [32.9756, -96.8897],
                    'beaumont': [30.0802, -94.1266],
                    'round rock': [30.5083, -97.6789],
                    'waco': [31.5493, -97.1467],
                    'denton': [33.2148, -97.1331],
                    'midland': [31.9973, -102.0779],
                    'wichita falls': [33.9137, -98.4934]
            }
        elif state.lower() == 'california':
                city_coordinates = {
                        "los angeles": [34.0522, -118.2437],
                        "san diego": [32.7157, -117.1611],
                        "san francisco": [37.7749, -122.4194],
                        "san jose": [37.3382, -121.8863],
                        "fresno": [36.7372, -119.7871],
                        "sacramento": [38.5816, -121.4944],
                        "long beach": [33.7701, -118.1937],
                        "oakland": [37.8044, -122.2711],
                        "bakersfield": [35.3733, -119.0187],
                        "anaheim": [33.8366, -117.9143],
                        "santa ana": [33.7456, -117.8677],
                        "riverside": [33.9806, -117.3755],
                        "stockton": [37.9577, -121.2908],
                        "irvine": [33.6846, -117.8265],
                        "fremont": [37.5485, -121.9886],
                        "san bernardino": [34.1083, -117.2898],
                        "modesto": [37.6391, -120.9969],
                        "fontana": [34.0922, -117.435],
                        "moreno valley": [33.9425, -117.2297],
                        "glendale": [34.1425, -118.2551],
                        "huntington beach": [33.6603, -117.9992],
                        "santa clarita": [34.3917, -118.5426],
                        "oxnard": [34.1975, -119.1771],
                        "garden grove": [33.7739, -117.9414],
                        "riverside": [33.9534, -117.3962],
                        "santa rosa": [38.4405, -122.7141],
                        "elk grove": [38.4088, -121.3716],
                        "corona": [33.8753, -117.5664],
                        "lancaster": [34.6868, -118.1542],
                        "palmdale": [34.5794, -118.1165]
                }
        
        try:
                return city_coordinates.get(city.lower())
        except:
                return None