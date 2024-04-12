import streamlit as st
from openai import OpenAI

client = OpenAI()

# Simulated image URLs or local paths
image_groups = {
    "Animals": [("https://images.unsplash.com/photo-1608848461950-0fe51dfc41cb?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxleHBsb3JlLWZlZWR8MXx8fGVufDB8fHx8fA%3D%3D","cat"), ("https://robustrecipes.com/wp-content/uploads/2021/03/Meet-Koda-We-Got-a-Puppy-7.jpg","Puppy"), ("https://upload.wikimedia.org/wikipedia/commons/0/08/Corl0207_%2828225976491%29.jpg","shark")],
    "Cars": [("https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/1974_Lancia_Stratos_Stradale_at_Greenwich_2021%2C_front_left.jpg/2560px-1974_Lancia_Stratos_Stradale_at_Greenwich_2021%2C_front_left.jpg","historic rally car"), ("https://slewhousemotorsport.com/cdn/shop/products/Photo_Jan_16_6_21_36_AM_1024x1024.jpg?v=1696290671","off road racing truck"), ("https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/2021_Citroen_Ami.jpg/2560px-2021_Citroen_Ami.jpg","small eco friendly city car")],
    "Nature": [("https://i.natgeofe.com/n/4a4a5beb-fd87-4c5d-9d76-4f9848ee15a4/14089898.jpg","mountain range in south america"), ("https://lp-cms-production.imgix.net/2019-06/e1401999dfdfedffdc8d1c2974bfb83b-sao-tome-principe.jpg","rainforest in Africa"), ("https://www.thetreecenter.com/c/uploads/2014/09/Cherry_Blossoms_1-scaled.webp","cherry blossom tree")],
    "Technology": [("https://m.media-amazon.com/images/I/71vYeYqdvUL._AC_UF894,1000_QL80_.jpg","computer printer"), ("https://assets.bwbx.io/images/users/iqjWHBFdfxIU/i8u4MyUMbqn0/v1/1200x800.jpg","vr headset"), ("https://mrleica.com/wp-content/uploads/2015/09/hasselblad-501cm.jpg","classic film camera")],
    "Food": [("https://joyfoodsunshine.com/wp-content/uploads/2021/05/kale-salad-recipe-3-500x500.jpg","kale salad"), ("https://www.southernliving.com/thmb/dnsycw_-mf35yKRkq3cBsThVzrY=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Southern-Living_Macarons_025-0e05e0cd226d44609f55ed8bc9cd3a3e.jpg","macarons dessert"), ("https://thefoodcharlatan.com/wp-content/uploads/2021/08/Homemade-Pizza-Recipe-1-Hour-or-Overnight-20.jpg","pepperoni pizza")]
}

# Function to display images and capture selections with checkboxes
def display_images(category, images):
    st.write(f"### {category}")
    cols = st.columns(3)
    for i, (url, label) in enumerate(images):
        with cols[i]:
            st.image(url, width=200)  # Display the image
            # Use a checkbox for selection
            if st.checkbox("Select", key=f"{category}_{i}"):
                # If selected, add the label to the user profile if it's not already added
                if label not in user_profile:
                    user_profile.append(label)

# User profile stored in session state to persist data across reruns
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = []

user_profile = st.session_state.user_profile

# Display all image groups
for category, images in image_groups.items():
    display_images(category, images)

# Submit button to finalize choices
if st.button("Submit"):
    # Display user profile
    st.write("## Your Selected Interests:")
    st.write(user_profile)
    
    sys_prompt = 'Act as a marketing analyst for my tech company.'
    
    init_prompt = 'Given the following list of interests from a high school student, generate a possible customer profile as well as a slogan that may appeal to them: ' + user_profile[0] + ", " + user_profile[1] + ", " + user_profile[2] + ", " + user_profile[3]
    
    response = client.chat.completions.create(
      model="gpt-4-turbo-preview",
      messages=[
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": init_prompt}
      ]
    )
    
    st.write(response.choices[0].message.content)
    
    
demo_info = st.text_area("Ad to generate...")
if st.button("Generate ad"):
    
    response = client.images.generate(
      model="dall-e-3",
      prompt=demo_info,
      size="1024x1024",
      quality="standard",
      n=1,
    )

    image_url = response.data[0].url
    st.image(image_url, width=600)