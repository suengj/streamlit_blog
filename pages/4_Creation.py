from utils import myFunc as my
from utils import llm_dict
from dotenv import load_dotenv

import os, json, time, requests
from datetime import datetime
import streamlit as st

from lumaai import LumaAI, AsyncLumaAI # for image creation

def main():

    st.set_page_config(
        page_title = "Generators",
        page_icon = "",
        layout="wide",
        initial_sidebar_state="expanded")

    st.header("Image/Video 생성")

    # side
    st.sidebar.title("Image/Video Generation Agent")

    my.sidebar_sublist() # sidebar sub list
    
    st.sidebar.markdown("---") # section 1

    LLM_LIST = ['Luma AI'] # 변경 필요
    
    _llm_to_use = st.sidebar.selectbox('선택할 LLM', LLM_LIST)

    # model selection
    LLM_MODEL = llm_dict.LLM_DICT[_llm_to_use]['MODEL']
    _model_to_use = st.sidebar.selectbox('선택할 모델', LLM_MODEL)

    # API connection
    API_KEY = llm_dict.LLM_DICT[_llm_to_use]['API']
    _api_to_use = my.api_key_loader(API_KEY)
    
    st.sidebar.markdown("---") # section 2

    history_md = """
    ### Notice
    
    Video : **Ray-2 Model should be updated**; the current version of Python Library not supports Ray-2 and other options
    """
    st.markdown(history_md)

    # MAIN PAGE
    col1, col2, col3 = st.columns([1,2,1])  # section separated

    # Luma AI to use
    if _llm_to_use == LLM_LIST[0]: # Luma AI selected

        if 'ray-2' not in _model_to_use: # if photo model
    
            with col1:
                # aspect ratio
                _aspect_list = ["1:1", "3:4", "4:3", "9:16", "16:9", "9:21", "21:9"]
                _aspect_to_use = st.selectbox('Select Aspect Ratio for creation', _aspect_list)
    
                st.markdown("---")
    
                _img_ref_dict = None
                _img_style_dict = None
                _img_mod_dict = None
    
                # Image Tuning reset
                if st.button("Reset Image options"):
                    st.session_state["ImageTuning"] = []
                    _img_ref_dict = None
                    _img_style_dict = None
                    _img_mod_dict = None
                    
                if "ImageTuning" not in st.session_state:
                    st.session_state["ImageTuning"] = []
    
                # image URL for reference
                _url_str = st.text_input(
                    "Please input URL if you need",
                    "",
                    key="TuningURL", # key - session_state.key 값으로 붙음
                )
    
                ImageOption_list = ["reference", "style", "modifications"]
                st.radio(
                    "Setting prompt option",
                    key = "imageOption",
                    options = ImageOption_list, # character options 별도로 빼기
                )
    
                # _url_rate = st.number_input('value input', min_value=0.0, max_value=5.0)
                _url_bar = st.slider('value select', 0.0, 1.0, (0.1))
    
                if st.button("Add to dictionary"):
                    if st.session_state.imageOption and _url_bar:
    
                        opt_dict = [{
                            "ImageOption": st.session_state.imageOption,
                            "OptionValue": _url_bar,
                            "TuningURL": _url_str
                        }]
    
                        st.session_state['ImageTuning'].append(opt_dict)
    
                # st.write(st.session_state['ImageTuning']) # session updates
    
                # Retrieve the last values - need to make function
                last_reference = next(
                    (entry[0] for entry in reversed(st.session_state['ImageTuning']) 
                     if entry[0]['ImageOption'] == ImageOption_list[0]), 
                    None
                ) # select the last reference option value and tuning URL
    
                last_style = next(
                    (entry[0] for entry in reversed(st.session_state['ImageTuning'])
                     if entry[0]['ImageOption'] == ImageOption_list[1]),
                    None
                ) # select the last style options
    
                last_modification = next(
                    (entry[0] for entry in reversed(st.session_state['ImageTuning'])
                     if entry[0]['ImageOption'] == ImageOption_list[2]),
                    None
                )
    
                st.markdown("**Reference Option will be applied:**")
    
                if last_reference:
                    _img_ref_dict = {
                        "url": last_reference['TuningURL'],
                        "weight": last_reference['OptionValue']
                    }
                    st.write(_img_ref_dict)
    
                st.markdown("**Style Option will be applied:**")
    
                if last_style:
                    _img_style_dict = {
                        "url": last_style['TuningURL'],
                        "weight": last_style['OptionValue']
                    }
                    st.write(_img_style_dict)
    
                st.markdown("**Modification Option will be applied:**")
    
                if last_modification:
                    _img_mod_dict = {
                        "url": last_modification['TuningURL'],
                        "weight": last_modification['OptionValue']
                    }
                    st.write(_img_mod_dict)
    
            with col2:
                LumaClient = LumaAI(auth_token = _api_to_use)

                # Ensure session state exists
                if "image_generation" not in st.session_state:
                    st.session_state["image_generation"] = [{"image_content": "이미지/비디오 생성",
                                                             "image_url": "현재는 비어있음"}]
        
                if "generation_history" not in st.session_state:
                    st.session_state["generation_history"] = []
        
                if st.sidebar.button("clear generation chat"):
                    st.session_state["image_generation"] = [{"image_content": "이미지/비디오 생성",
                                                             "image_url": "현재는 비어있음"}]
                    
                    st.sidebar.success("Generation Chat cleared")
        
                if st.sidebar.button("clear generation history"):
                    st.session_state["generation_history"] = []
                    st.sidebar.success("Generation History Cleared!")
                
                # Display conversation history
                for gen in st.session_state["image_generation"]:
                    st.markdown(gen["image_content"])
                    # st.image(gen['image_url'], width=200)
                
                # Process new user input
                if prompt := st.chat_input(placeholder="원하는 이미지가 무엇인가요?"):
                    # Add user message to the session
                    st.session_state["image_generation"].append({"image_content": prompt})
                    
                    with st.chat_message("user"):
                        st.markdown(prompt)
                
                    try: # Luma AI
        
                        with st.chat_message("assistant"):
    
                            generation = LumaClient.generations.image.create(
                                prompt = prompt,
                                model = _model_to_use,
                                aspect_ratio = _aspect_to_use,
                                image_ref = _img_ref_dict,
                                style_ref = _img_style_dict,
                                modify_image_ref = _img_mod_dict,
                                # character_ref = _chr_ref
                            )
    
                            _placeholder = st.empty()
                            start_time = time.time()
    
                            completed=False
                            while not completed:
                                generation = LumaClient.generations.get(id = generation.id)
                                if generation.state == "completed":
                                    completed = True
    
                                elif generation.state == "failed":
                                    raise RuntimeError(f"Generation failed: {generation.failure_reason}")
    
                                _placeholder.write(f"Processing: {time.time()-start_time:.1f} sec. Please wait...")
    
                            image_url = generation.assets.image
                            _placeholder.empty()
    
                            st.image(image_url)
    
                            st.write(f"Image Generated in {time.time()-start_time: .2f} seconds")
                            st.session_state["image_generation"].append(
                                {"image_content": prompt,
                                "image_url": image_url})
        
                            st.session_state["generation_history"].append(
                                {'image_query': prompt,
                                'image_url': image_url}
                            )
    
                            # session updates
                            # download the image to the local
                            image_response = requests.get(image_url,
                                                          stream=True)
    
                            if image_response.status_code == 200:
                                image_data = image_response.content
    
                                st.download_button(
                                    label = "Download Image",
                                    data = image_data,
                                    file_name = f"{generation.id}.jpg",
                                    mime = "image/jpg"
                                )
                            else:
                                st.error("Failted to fetch the image")
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    
            with col3:
                    
                st.write("### Generation history")

                try:
                    for entry in st.session_state['generation_history']:
                        st.write(f"-**QUERY**: {entry['image_query']}")
                        st.write(f"-**IMAGE URL**: {entry['image_url']}")
                        st.image(entry['image_url'],width=200)

                except:
                    st.write("No history")
        
        # video section
        elif 'ray-2' in _model_to_use:
                
            with col1:
                # aspect ratio
                _aspect_list = ["1:1", "3:4", "4:3", "9:16", "16:9", "9:21", "21:9"]
                _aspect_to_use = st.selectbox('Select Aspect Ratio for creation', _aspect_list)

                # resoultion
                _resolution_list = ["540p", "720p"] # to be updated
                _resolution_to_use = st.selectbox('Select Resolution',_resolution_list)

                # duration
                _duration_to_use = st.slider('time sec. select', 5.0, 9.9)

                # loop (state_session)
                st.checkbox("Loop Mode", key="loop")
                _loop = st.session_state.loop
                st.write(st.session_state.loop)

                # Image Tuning reset
                if st.button("Reset Video options"):
                    st.session_state["KeyFrames"] = []
                    _keyframes_dict = None
                    
                if "KeyFrames" not in st.session_state:
                    st.session_state["KeyFrames"] = []
                    st.session_state["frameOptions"] = "frame0"
                    st.session_state["videoTypeOptions"] = "image"
    
                keyframe_list = ["frame0", "frame1"]
                st.radio(
                    "Setting key frame option",
                    key = "frameOptions",
                    options = keyframe_list,
                )

                videotype_list = ["image","generation"]
                st.radio(
                    "Setting Video Type Option",
                    key = "videoTypeOptions",
                    options = videotype_list,
                )

                # image URL for reference
                _url_vid_str = st.text_input(
                    "Please input URL / Video ID if you need",
                    "",
                    key="URL_VID", # key - session_state.key 값으로 붙음
                )
    
                if st.button("Add to dictionary"):
                    if st.session_state.frameOptions and st.session_state.videoTypeOptions and _url_vid_str: # all values input

                        opt_dict = {
                            st.session_state.frameOptions:
                            {
                                "type": st.session_state.frameOptions,
                                "url" if st.session_state.videoTypeOptions == videotype_list[0] else "id" if st.session_state.videoTypeOptions == videotype_list[1] else "none": _url_vid_str
                            }
                        }
    
                        st.session_state['KeyFrames'].append(opt_dict)

                st.write(st.session_state['KeyFrames'])

                _keyframes_dict = {}
                    
                # Key Frame creation
                if st.button("Click to create video Options") and len(st.session_state['KeyFrames'])>0:
                    _keyframes_dict = {key: value for item in st.session_state['KeyFrames'] for key, value in item.items()}
                    # if key is same, the values are merged; Currently interpolate between 2 videos cannot be

                st.write(_keyframes_dict)

            with col2:
                LumaClient = LumaAI(auth_token = _api_to_use)
    
                # Ensure session state exists
                if "video_generation" not in st.session_state:
                    st.session_state["video_generation"] = [{"video_content": "비디오 생성",
                                                             "video_url": "현재는 비어있음"}]
        
                if "generation_history" not in st.session_state:
                    st.session_state["generation_history"] = []
        
                if st.sidebar.button("clear generation chat"):
                    st.session_state["video_generation"] = [{"video_content": "비디오 생성",
                                                             "video_url": "현재는 비어있음"}]
                    
                    st.sidebar.success("Generation Chat cleared")
        
                if st.sidebar.button("clear generation history"):
                    st.session_state["generation_history"] = []
                    st.sidebar.success("Generation History Cleared!")
                
                # Display conversation history
                for gen in st.session_state["video_generation"]:
                    st.markdown(gen["video_content"])
                    # st.image(gen['image_url'], width=200)
                
                # Process new user input
                if prompt := st.chat_input(placeholder="원하는 비디오가 무엇인가요?"):
                    # Add user message to the session
                    st.session_state["video_generation"].append({"video_content": prompt})
                    
                    with st.chat_message("user"):
                        st.markdown(prompt)
                
                    try: # Luma AI
        
                        with st.chat_message("assistant"):
    
                            generation = LumaClient.generations.create(
                                prompt = prompt,
                                # model = _model_to_use,
                                # resolution = _resolution_to_use,
                                # duration = _duration_to_use,
                                aspect_ratio = _aspect_to_use,
                                loop = _loop,
                                # keyframes = _keyframes_dict,
                            )
    
                            _placeholder = st.empty()
                            start_time = time.time()
    
                            completed=False
                            while not completed:
                                generation = LumaClient.generations.get(id = generation.id)
                                if generation.state == "completed":
                                    completed = True
    
                                elif generation.state == "failed":
                                    raise RuntimeError(f"Generation failed: {generation.failure_reason}")
    
                                _placeholder.write(f"Processing: {time.time()-start_time:.1f} sec. Please wait...")
    
                            video_url = generation.assets.video
                            _placeholder.empty()
    
                            st.video(video_url)
    
                            st.write(f"Image Generated in {time.time()-start_time: .2f} seconds")
                            st.session_state["video_generation"].append(
                                {"video_content": prompt,
                                "video_url": video_url})
        
                            st.session_state["generation_history"].append(
                                {'video_query': prompt,
                                'video_url': video_url}
                            )
    
                            # session updates
                            # download the image to the local
                            video_response = requests.get(video_url,
                                                          stream=True)
    
                            if video_response.status_code == 200:
                                video_data = video_response.content
    
                                st.download_button(
                                    label = "Download Video",
                                    data = video_data,
                                    file_name = f"{generation.id}.mp4",
                                    mime = "video/mp4"
                                )
                            else:
                                st.error("Failted to generate the video")
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    
            with col3:
                    
                st.write("### Generation history")
                
                try:
                    for entry in st.session_state['generation_history']:
                        st.write(f"-**QUERY**: {entry['video_query']}")
                        st.write(f"-**VIDEO URL**: {entry['video_url']}")
                        st.video(entry['video_url'])

                except:
                    st.write("No history")
            

    else:
        st.write("None of model is selected")

if __name__ == "__main__" :
    main()

# end of code