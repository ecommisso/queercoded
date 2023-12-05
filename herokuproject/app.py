from flask import Flask, render_template, request, redirect, url_for
import os
import json
from PIL import Image
from io import BytesIO
import base64
import time


app = Flask(__name__, static_url_path='/static')
upload_folder = 'static/drawings'
app.config['UPLOAD_FOLDER'] = upload_folder


history_data = {
    "Jane Addams": {
        "text": "Jane Addams wore many hats in the late 19th and early 20th centuries: suffragist, social worker, activist, Nobel Peace Prize recipient. Notably, Addams founded Chicago's Hull House in 1889, a time when many new immigrants lived and worked in harsh conditions. This settlement house provided health care, day care, education, vocational training, cultural and social activities, and legal aid to the immigrant community, creating a new model for social welfare. Addams maintained a decades-long relationship with philanthropist Mary Rozet Smith, marked by loving letters.",
        "image_path": "images/jane_addams.png", 
    },
     "Josephine Baker": {
        "text": "Entertainer and activist Josephine Baker performed in vaudeville showcases and in Broadway musicals, including Shuffle Along. In 1925, she moved to Paris to perform in a revue. When the show closed, Baker was given her own show and found stardom. She became the first African American woman to star in a motion picture and to perform with an integrated cast at an American concert hall. At the March on Washington in 1968, Baker was the only woman speaker. In her speech, she honored fellow women civil rights activists. She had relationships with both men and women throughout her lifetime.",
        "image_path": "images/josephine_baker.png", 
    },
    "Chavela Vargas": {
        "text": "Chavela Vargas was a Mexican ranchera singer who was openly lesbian and became an LGBTQ+ icon in Mexico and beyond. Her music and life challenged gender norms and paved the way for greater acceptance of LGBTQ+ individuals in the Latinx community.",
        "image_path": "images/chavela_vargas.png", 
    },
    "Stormé DeLarverie": {
        "text": "Stormé DeLarverie was a black butch lesbian who was active in the bar culture of New York City. She performed in the first racially integrated drag revue in the U.S. as the group's only drag king and is famous for her role in the Stonewall riots. According to many (including DeLarverie herself), she threw the first punch at Stonewall and was the catalyst for sparking the rebellion. She was active in the LGBT rights movement after Stonewall and worked as a bouncer at lesbian bars for many years. She passed away at age 93 in 2014 and was referred to as a 'gay superhero' in her New York Times obituary.",
        "image_path": "images/storme_delarverie.png", 
    },
     "Rosalie \"Rose\" Bamberger": {
        "text": "Rosalie \"Rose\" Bamberger (1921-1990), who had the initial idea to form a private lesbian social club. The four founding couples first met at Rose and Rosemary's house on September 21, 1955. The founding meeting included Rose and her partner Rosemary Sliepen, as well as couples Del Martin and Phyllis Lyon, Marcia Foster and her partner June, and Noni Frey and her partner Mary. Rose and Rosemary were working class and both employed in brush-manufacturing factories. While they left the DOB in January 1956, both Rose and Rosemary were still on the mailing list of Del and Phyllis into the 1970s. Census records and city directories show that Rosalie and Rosemary continued to live together until Rosalie's death in 1990. Rosemary passed away in 2010. Unfortunately, there are no public images of her, so here we have used the cover of The Ladder, a publication established by the Daughters of Bilitis.",
        "image_path": "images/daughters_of_bilitis.jpeg", 
    },
    "Del Martin and Phyllis Lyon": {
        "text": "Del Martin and Phyllis Lyon were a lesbian couple who co-founded the Daughters of Bilitis in 1955, the first lesbian organization in the United States. They were also advocates for marriage equality and were among the first same-sex couples to legally marry in California when it briefly became legal in 2008.",
        "image_path": "images/del_martin_and_phyllis_lyon.png", 
    },
    "Edith \"Edie\" Windsor": {
        "text": "Edie Windsor made history when her case United States v. Windsor overturned part of the Defense of Marriage Act, a landmark victory in the fight for same-sex marriage. Windsor filed the case after her longtime partner Thea Spyer passed away, and Windsor was unable to claim spousal exemptions over Spyer's estate because 'spouse' only applied to heterosexual marriages. The Supreme Court ruled in her favor, effectively putting the final nails in DOMA's coffin. Windsor was also active in a wide range of other LGBTQ+ causes and, as a former IBM employee, was very involved in the tech world. She passed away in 2017 at the age of 88.",
        "image_path": "images/edie_windsor.png", 
    },
    "Lorraine Hansberry": {
        "text": "Playwright, writer, and activist Lorraine Hansberry is best known for her Broadway play and later film, A Raisin in the Sun. She was inspired by her family's landmark court case against Chicago's discriminatory real estate laws. Hansberry participated in civil rights demonstrations and the communist movement throughout her lifetime. Though she married her closest friend, Robert Nemiroff, she secretly affirmed her homosexuality in her letters and unpublished short stories. Her life was cut short from pancreatic cancer at age 34 on January 12, 1965.",
        "image_path": "images/lorraine_hansberry.png", 
    },
    "Barbara Smith": {
        "text": "Barbara Smith is a black lesbian activist, writer, and educator who was influential in the development of black feminism. As a young woman, she was involved in the Civil Rights Movement and helped establish the Combahee River Collective in 1975, an organization of black lesbian feminists that was active until 1980. She then founded Kitchen Table: Women of Color Press with other lesbians of color, including Audre Lorde, June Jordan, and Gloria Anzaldúa. The press was created to promote works by women of color, and they published influential texts including 'This Bridge Called My Back' and 'I Am Your Sister: Black Women Organizing Across Sexualities.'",
        "image_path": "images/barbara_smith.png", 
    },
    "Barbara Gittings": {
        "text": "Barbara Gittings was a lesbian activist and one of the early leaders of the LGBTQ+ rights movement in the United States. She co-founded the Daughters of Bilitis, one of the first lesbian organizations in the country, and was involved in advocating for the removal of homosexuality from the American Psychiatric Association's list of mental disorders.",
        "image_path": "images/barbara_gittings.png", 
    },
    "Audre Lorde": {
        "text": "Audre Lorde was a Black lesbian poet, writer, and civil rights activist. Her writings, such as 'Sister Outsider' and 'Zami: A New Spelling of My Name,' explored themes of race, gender, and sexuality. Lorde's work has had a profound impact on intersectional feminism and LGBTQ+ literature. She also earned a master's degree in library science at my school, Columbia University.",
        "image_path": "images/audre_lorde.png",
    },
     "Dr. Renée Richards": {
        "text": "Dr. Renée Richards: ophthalmologist, former tennis player, and one of the first professional athletes to identify as transgender. In 1976, following Richards' sex reassignment surgery, the U.S. Tennis Association required her to undergo genetic screening to play at the U.S. Open as a woman. Richards refused and was barred from the tournament. She then sued the U.S. Tennis Association for gender discrimination and won in a landmark decision. The following year, Richards was admitted to play in U.S. Open, where she reached the final in women's doubles tournament.",
        "image_path": "images/renee_richards.png", 
    },
    "Gloria Evangelina Anzaldúa": {
         "text": "Gloria Evangelina Anzaldúa was a political activist, feminist, academic, and perhaps one of the most important queer Latina writers of all time. Anzaldúa explored the theories of feminism and homosexuality and how to navigate between her queer and Chicana identity. \"Borderlands/La Frontera: The New Mestiza\" is one of her most recognized works for being an important part of feminist and Chicana/o studies, along with the co-editing of \"This Bridge Called My Back: Writings by Radical Women of Color\". ",
         "image_path": "images/gloria_anzaldua.png",   
     },
    "Marsha P. Johnson": {
        "text": "Marsha P. Johnson was a transgender woman of color and a prominent figure in the LGBTQ+ rights movement. She is often credited with being one of the key figures in the Stonewall riots of 1969, which sparked the modern LGBTQ+ rights movement. Johnson co-founded the Gay Liberation Front and the Street Transvestite Action Revolutionaries (STAR) with Sylvia Rivera to advocate for transgender and homeless individuals.",
        "image_path": "images/marsha_p_johnson.png", 
    },
    "Tamara Ching": {
        "text": "Tamara Ching (1949-) is an advocate, activist, and former sex worker. Ching made her gender transition in the late seventies, while working for the Community Services Administration under President Carter. She was an original member of the Transgender Advisors to the San Francisco Human Rights Commission and served as advisor on transgender issues to numerous city political bodies and agencies, including the Board of Supervisors, the San Francisco Police Department, and the Department of Public Health. Ching has also worked in AIDS education outreach, managed a support group for Asian and Pacific Islander trans people, and investigated allegations of discrimination for the Transgender Services Commission.",
        "image_path": "images/tamara_ching.png", 
    },
    "Sylvia Rivera": {
        "text": "Sylvia Rivera was a transgender activist and close friend of Marsha P. Johnson. She co-founded the Gay Liberation Front and the Street Transvestite Action Revolutionaries (STAR) with Johnson. Rivera was a strong advocate for the inclusion of transgender and gender-nonconforming people in the LGBTQ+ movement.", 
        "image_path": "images/sylvia_rivera.png", 
    },
    "Kitty Tsui": {
        "text": "Kitty Tsui:  (born 1952) is an American author, poet, actor, and bodybuilder. She was the first known Asian American lesbian to publish a book (Words of a Woman who Breathes Fire, published in 1983).",
        "image_path": "images/kitty_tsui.png", 
    },
    "Hulleah Tsinhnahjinnie": {
        "text": "Hulleah Tsinhnahjinnie is a Two Spirit photographer and curator known for her artwork depicting Native women and families, urban Native people, and Indigenous responses to colonialist history. She was born into the bear and raccoon clans of the Seminole and Muscogee nations and born for the Tsinajinnie clan of the Navajo Nation. She is active in several Native American organizations and continues to document Indigenous community gatherings and acts of activism and sovereignty in northern California. She works as Professor of Native American Studies at UC Davis and Director of the C.N. Gorman Museum.",
        "image_path": "images/hulleah_tsinhnahjinnie.png", 
    },
    "Cecilia Chung": {
        "text": "Cecilia Chung works to advocate for human rights, social justice, health equity, and LGBT equality. Chung was born in Hong Kong. She has lived in San Francisco since 1984. Today she works as the Director of Evaluation and Strategic Initiatives at Transgender Law Center. In 2008, she became the first transgender woman and first person living openly with HIV to chair the San Francisco Human Rights Commission.",
        "image_path": "images/cecilia_chung.png", 
    },  
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/history')
def history():
    return render_template('history.html', data=history_data)

dir_path = 'stories/'
if not os.path.exists(dir_path):
    print("making the ../stories dir")
    os.makedirs(dir_path)

@app.route('/user_story', methods=['GET', 'POST'])
def user_story():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_input = request.form.get('user_input')
        drawing_image_data = request.form.get('drawing_image')

        print("DRAWING: ", drawing_image_data)

        # use anon if name is not provided
        user_data = {
            'name': user_name if user_name else 'Anonymous',
            'story': user_input,
            'image_path': save_drawing_image(drawing_image_data),
        }

       # read existing json
        json_file_path = os.path.join(dir_path, "users.json")
        user_data_list = []

        if os.path.exists(json_file_path) and os.stat(json_file_path).st_size > 0:
            with open(json_file_path, "r") as json_file:
                user_data_list = json.load(json_file)

        # add to front so it shows up first
        user_data_list.insert(0, user_data)

        with open(json_file_path, "w") as json_file:
            json.dump(user_data_list, json_file)

        # # Handle drawing image data
        # if drawing_image_data:
        #     save_drawing_image(drawing_image_data)

        # Redirect to the same page to avoid form resubmission on page refresh
        return redirect(url_for('user_story'))
    
    json_file_path = os.path.join(dir_path, "users.json")
    user_stories = []

    if os.path.exists(json_file_path) and os.stat(json_file_path).st_size > 0:
        with open(json_file_path, "r") as json_file:
            for line in json_file:
                entry = json.loads(line)
                for item in entry: 
                    name = item['name']
                    story = item['story']
                    image_path = item['image_path']
                    user_stories.append({'name': name, 'story': story, 'image_path': image_path})


    return render_template('user_story.html', user_stories=user_stories)

def save_drawing_image(drawing_image_data):
    # Extract the base64-encoded image data
    _, encoded_data = drawing_image_data.split(",", 1)
    image_data = base64.b64decode(encoded_data)

    image = Image.open(BytesIO(image_data))

    # Create static/drawings if DNE
    upload_folder = app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)

    # Save the image with unique timestamp
    filename = f"{int(time.time())}.png"
    image_path = os.path.join(upload_folder, filename)

    print("PATH", image_path)
    print("filename", filename)
    image.save(image_path)
    
    return os.path.join("drawings", filename)

@app.route('/resources')
def resources():
    return render_template('resources.html')


# run using: flask --app app run
if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 3000)