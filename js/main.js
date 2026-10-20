(() => {
  'use strict';

  const WHATSAPP_NUMBER = '254113111330';
  const formatKSh = (amount) => `KSh ${amount.toLocaleString('en-US')}`;

  const products = [
    /* ---- Weight Management (In-Stock flyer) ---- */
    {
      name: 'Tirzzy 5 mg',
      category: 'Weight Management',
      price: 5000,
      image: 'assets/img/products/tirzzy-5.jpg',
      badge: 'Bestseller',
      description: 'The entry strength of our flagship Tirzzy peptide — 5 mg per sealed vial and the most-ordered size in the range.'
    },
    {
      name: 'Tirzzy 10 mg',
      category: 'Weight Management',
      price: 10000,
      image: 'assets/img/products/tirzzy-10.jpg',
      badge: 'Popular',
      description: 'The go-to Tirzzy strength — 10 mg per lyophilised vial, shipped sealed with a handling and reconstitution guide.'
    },
    {
      name: 'Tirzzy 15 mg',
      category: 'Weight Management',
      price: 13000,
      image: 'assets/img/products/tirzzy-15.jpg',
      badge: 'In stock',
      description: 'A step-up Tirzzy dose at 15 mg per vial — popular with returning customers moving up from the 10 mg size.'
    },
    {
      name: 'Tirzzy 20 mg',
      category: 'Weight Management',
      price: 17000,
      image: 'assets/img/products/tirzzy-20.jpg',
      badge: 'In stock',
      description: 'The standard advanced Tirzzy strength — 20 mg per sealed vial with a clear reconstitution guide in every box.'
    },
    {
      name: 'Tirzzy 30 mg',
      category: 'Weight Management',
      price: 23000,
      image: 'assets/img/products/tirzzy-30.jpg',
      badge: 'In stock',
      description: 'A higher 30 mg Tirzzy dose for established protocols. Ask our team to confirm current stock before ordering.'
    },
    {
      name: 'Tirzzy 60 mg',
      category: 'Weight Management',
      price: 40000,
      image: 'assets/img/products/tirzzy-60.jpg',
      badge: 'Top strength',
      description: 'The top of the Tirzzy range — 60 mg per vial and our best value per milligram. Available while stocks last.'
    },
    {
      name: 'RETA 5 mg',
      category: 'Weight Management',
      price: 10000,
      image: 'assets/img/products/reta-5.jpg',
      badge: 'New',
      description: 'RETA research peptide at 5 mg per vial — a newer, single-vial introduction to our advanced weight line.'
    },
    {
      name: 'RETA 10 mg',
      category: 'Weight Management',
      price: 20000,
      image: 'assets/img/products/reta-10.jpg',
      badge: 'Advanced',
      description: 'Double-strength RETA, 10 mg per sealed vial for established protocols, with the same lab-tested quality as the range.'
    },
    {
      name: '5 AMINO 10 mg',
      category: 'Weight Management',
      price: 4000,
      image: 'assets/img/products/amino-10.jpg',
      badge: 'In stock',
      description: '5-Amino-1MQ research compound, 10 mg per vial — a metabolic-pathway favourite with beginner-friendly pricing.'
    },

    /* ---- Energy & Endurance ---- */
    {
      name: 'MOTS-C 5 mg',
      category: 'Energy & Endurance',
      price: 4000,
      image: 'assets/img/products/mots-5.jpg',
      badge: 'In stock',
      description: 'MOTS-C mitochondrial research peptide in a 5 mg starting vial — the accessible entry point to the line.'
    },
    {
      name: 'MOTS-C 10 mg',
      category: 'Energy & Endurance',
      price: 7000,
      image: 'assets/img/products/mots-10.jpg',
      badge: 'Popular',
      description: 'MOTS-C at 10 mg per vial, lyophilised and sealed, with a storage card included in every box.'
    },
    {
      name: 'NAD+ 100 mg',
      category: 'Energy & Endurance',
      price: 3000,
      image: 'assets/img/products/nad-100.jpg',
      badge: 'Best value',
      description: 'NAD+ research formula, 100 mg per vial — one of the best-value lines in the whole in-stock catalogue.'
    },
    {
      name: 'SS-31 5 mg',
      category: 'Energy & Endurance',
      price: 3000,
      image: 'assets/img/products/ss31-5.jpg',
      badge: 'In stock',
      description: 'SS-31 (elamipretide) research peptide, 5 mg per sealed vial, from our cellular-health line.'
    },

    /* ---- Recovery & Repair ---- */
    {
      name: 'BPC-157 5 mg',
      category: 'Recovery & Repair',
      price: 3000,
      image: 'assets/img/products/bpc-157.jpg',
      badge: 'Bestseller',
      description: 'The most-requested recovery research peptide — 5 mg per lyophilised vial at a genuine value price.'
    },
    {
      name: 'KPV 10 mg',
      category: 'Recovery & Repair',
      price: 7000,
      image: 'assets/img/products/kpv-10.jpg',
      badge: 'In stock',
      description: 'KPV research peptide, 10 mg per vial — often paired with BPC-157 in recovery protocols.'
    },
    {
      name: 'EPITALON 10 mg',
      category: 'Recovery & Repair',
      price: 8000,
      image: 'assets/img/products/epitalon-10.jpg',
      badge: 'In stock',
      description: 'Epitalon research peptide, 10 mg per sealed vial — a longevity-pathway favourite, batch-tested before dispatch.'
    },
    {
      name: 'TESA 5 mg',
      category: 'Recovery & Repair',
      price: 7000,
      image: 'assets/img/products/tesa-5.jpg',
      badge: 'New',
      description: 'TESA research peptide, 5 mg per vial — newly added to the advanced recovery line. Ask us about current stock.'
    },

    /* ---- Glow & Immunity ---- */
    {
      name: 'GHK-CU 50 mg',
      category: 'Glow & Immunity',
      price: 8000,
      image: 'assets/img/products/ghk-cu.jpg',
      badge: 'Popular',
      description: 'GHK-Cu copper peptide, 50 mg per vial — instantly recognisable by its vivid blue powder. A skincare-research favourite.'
    },
    {
      name: 'Glutathione 600 mg',
      category: 'Glow & Immunity',
      price: 4000,
      image: 'assets/img/products/glutathione.jpg',
      badge: 'In stock',
      description: 'Glutathione 600 mg per vial — the antioxidant staple of our glow line, priced for everyday stacking.'
    },
    {
      name: 'Lipo-C Plain 10 mL',
      category: 'Glow & Immunity',
      price: 6000,
      image: 'assets/img/products/lipo-c.jpg',
      badge: 'In stock',
      description: 'Liposomal vitamin C in a 10 mL sealed vial — a luminous liquid formula with liposomal delivery for enhanced absorption.'
    },
    {
      name: 'Lipo-C with B12 10 mL',
      category: 'Glow & Immunity',
      price: 8000,
      image: 'assets/img/products/lipo-c-b12.jpg',
      badge: 'Popular',
      description: 'Liposomal vitamin C boosted with B12, 10 mL per sealed vial — our most popular immunity and energy add-on.'
    },

    /* ---- Focus & Performance ---- */
    {
      name: 'SEMAX 5 mg',
      category: 'Focus & Performance',
      price: 3000,
      image: 'assets/img/products/semax-5.jpg',
      badge: 'Popular',
      description: 'Semax research peptide, 5 mg per vial — the go-to choice in our focus line for cognitive protocols.'
    },
    {
      name: 'SELANK 5 mg',
      category: 'Focus & Performance',
      price: 3000,
      image: 'assets/img/products/selank-5.jpg',
      badge: 'In stock',
      description: 'Selank research peptide, 5 mg per vial — the calming counterpart to Semax in our nootropic line.'
    },
    {
      name: 'P141 (PT-141) 10 mg',
      category: 'Focus & Performance',
      price: 5000,
      image: 'assets/img/products/p141-10.jpg',
      badge: 'In stock',
      description: 'PT-141 (P141) research peptide, 10 mg per sealed vial from our performance line. Confirm batch availability first.'
    },

    /* ---- Reconstitution Supplies ---- */
    {
      name: 'BAC Water 3 mL',
      category: 'Reconstitution Supplies',
      price: 2000,
      image: 'assets/img/products/bac-water-3.jpg',
      badge: 'Essential',
      description: 'Sterile bacteriostatic water, 3 mL vial — the essential reconstitution partner for any peptide vial.'
    },
    {
      name: 'BAC Water 5 mL',
      category: 'Reconstitution Supplies',
      price: 3000,
      image: 'assets/img/products/bac-water-5.jpg',
      badge: 'Essential',
      description: 'Bacteriostatic water, 5 mL vial — the everyday size that suits most single-vial protocols.'
    },
    {
      name: 'BAC Water 10 mL',
      category: 'Reconstitution Supplies',
      price: 5000,
      image: 'assets/img/products/bac-water-10.jpg',
      badge: 'Best value',
      description: 'Bacteriostatic water, 10 mL vial — best value for multi-vial users. Sealed and sterile.'
    },
    {
      name: 'Acetic Acid 5 mL',
      category: 'Reconstitution Supplies',
      price: 4000,
      image: 'assets/img/products/acetic-acid.jpg',
      badge: 'Essential',
      description: 'Acetic acid, 5 mL — a specialist research supply used in some preparation protocols. Handle per your procedure.'
    }
  ];

  const counties = [
    'Mombasa', 'Kwale', 'Kilifi', 'Tana River', 'Lamu', 'Taita-Taveta',
    'Garissa', 'Wajir', 'Mandera', 'Marsabit', 'Isiolo', 'Meru',
    'Tharaka-Nithi', 'Embu', 'Kitui', 'Machakos', 'Makueni', 'Nyandarua',
    'Nyeri', 'Kirinyaga', "Murang'a", 'Kiambu', 'Turkana', 'West Pokot',
    'Samburu', 'Trans Nzoia', 'Uasin Gishu', 'Elgeyo-Marakwet', 'Nandi',
    'Baringo', 'Laikipia', 'Nakuru', 'Narok', 'Kajiado', 'Kericho', 'Bomet',
    'Kakamega', 'Vihiga', 'Bungoma', 'Busia', 'Siaya', 'Kisumu', 'Homa Bay',
    'Migori', 'Kisii', 'Nyamira', 'Nairobi'
  ];

  const reviews = [
    { name: 'Jane Wanjiku', town: 'Westlands', county: 'Nairobi', product: 'Tirzzy 10 mg', rating: 5, date: 'Oct 2026', text: 'Three weeks on Tirzzy 10 mg and my clothes fit better already. Delivery to Westlands took one day and the packaging is so beautiful I kept the box!' },
    { name: 'Brian Otieno', town: 'Milimani', county: 'Kisumu', product: 'MOTS-C 10 mg', rating: 5, date: 'Sep 2026', text: 'I drive long distances for work and my afternoons used to be a struggle. With MOTS-C I stay alert without the jitters of energy drinks. Highly recommended.' },
    { name: 'Faith Chebet', town: 'Eldoret', county: 'Uasin Gishu', product: 'Tirzzy 15 mg', rating: 5, date: 'Sep 2026', text: 'Late-night snacking was my biggest problem. Tirzzy 15 mg helped me feel full with smaller portions. Down 4kg in my first month, pole pole tu!' },
    { name: 'David Kamau', town: 'Thika', county: 'Kiambu', product: 'Tirzzy 30 mg', rating: 5, date: 'Aug 2026', text: 'Premium product, you can tell from the sealed packaging. My tummy is visibly flatter after six weeks combined with evening walks. Worth every shilling.' },
    { name: 'Grace Achieng', town: 'Homa Bay', county: 'Homa Bay', product: 'Tirzzy 5 mg', rating: 5, date: 'Sep 2026', text: 'My digestion and sleep have both improved since I started Tirzzy 5 mg. The team on WhatsApp explained everything patiently before I ordered. Asante sana!' },
    { name: 'Peter Mwangi', town: 'Milimani', county: 'Nakuru', product: 'Tirzzy 10 mg', rating: 4, date: 'Jul 2026', text: 'Good product and fast delivery to Nakuru. Results took about three weeks to show for me, so be patient and consistent. Would order again.' },
    { name: 'Mary Nekesa', town: 'Bungoma', county: 'Bungoma', product: 'Tirzzy 15 mg', rating: 5, date: 'Aug 2026', text: 'I was scared of fake products online but this came sealed with the Premium Supplements branding and a guide inside. Cravings for chapati and mandazi are gone!' },
    { name: 'Samuel Kiprop', town: 'Kericho', county: 'Kericho', product: 'MOTS-C 10 mg', rating: 5, date: 'Oct 2026', text: 'As a tea farmer I start work at 5am. MOTS-C keeps me going strong the whole day. My brother in Bomet has now ordered his too.' },
    { name: 'Lucy Moraa', town: 'Kisii', county: 'Kisii', product: 'Tirzzy 5 mg', rating: 5, date: 'Jun 2026', text: 'I feel lighter and more active, and my skin is glowing. The consultation before buying was free and very helpful. Genuine people.' },
    { name: 'James Ochieng', town: 'Bondo', county: 'Siaya', product: 'Tirzzy 10 mg', rating: 5, date: 'Sep 2026', text: 'Lost 6kg in 5 weeks with Tirzzy 10 mg plus skipping rope. Delivery reached Bondo in two days, well packed. I have recommended it to my chama group.' },
    { name: 'Ann Muthoni', town: 'Nyeri', county: 'Nyeri', product: 'Tirzzy 60 mg', rating: 5, date: 'Aug 2026', text: 'The full 60 mg course feels like pure luxury — sealed vials, a gold welcome card and a guide in a gift box. My appetite, energy and weight are all changing together.' },
    { name: 'Daniel Kimeu', town: 'Machakos', county: 'Machakos', product: 'Tirzzy 30 mg', rating: 4, date: 'May 2026', text: 'Strong formula, best for someone serious like me. Took off one star because I wanted faster delivery, but the product itself is excellent.' },
    { name: 'Sharon Awino', town: 'Migori', county: 'Migori', product: 'Tirzzy 15 mg', rating: 5, date: 'Sep 2026', text: "I eat half of what I used to and I don't feel punished. Tirzzy just switches off the constant food noise. My sister is ordering next week." },
    { name: 'Michael Njoroge', town: "Murang'a", county: "Murang'a", product: 'MOTS-C 10 mg', rating: 5, date: 'Jul 2026', text: "No more 2pm slump at the office. I feel steady energy from morning to evening. Delivery to Murang'a was quick and the parcel was discreet." },
    { name: 'Beatrice Cherono', town: 'Kapsabet', county: 'Nandi', product: 'Tirzzy 5 mg', rating: 5, date: 'Aug 2026', text: 'Tirzzy 5 mg sorted my bloating within two weeks. I feel comfortable in my clothes again. The WhatsApp follow-up after delivery was a nice touch.' },
    { name: 'Kevin Barasa', town: 'Busia', county: 'Busia', product: 'Tirzzy 10 mg', rating: 5, date: 'Oct 2026', text: 'I was doubtful, but the reviews convinced me and they were right. 5kg down and my face looks slimmer in photos. Genuine product, sealed and branded.' },
    { name: 'Ruth Wambui', town: 'Kerugoya', county: 'Kirinyaga', product: 'Tirzzy 15 mg', rating: 4, date: 'Jun 2026', text: 'Works well for portion control. First week I felt some nausea so I started with a smaller dose as advised, now I am fine. Good support team.' },
    { name: 'George Omondi', town: 'Mombasa', county: 'Mombasa', product: 'MOTS-C 10 mg', rating: 5, date: 'Sep 2026', text: 'Mombasa heat used to drain me by noon. MOTS-C keeps me fresh through the day. Delivery to the island took just one day!' },
    { name: 'Caroline Kilonzo', town: 'Wote', county: 'Makueni', product: 'Tirzzy 10 mg', rating: 5, date: 'Jul 2026', text: 'After two babies my tummy refused to go. Tirzzy 10 mg plus walking has flattened it nicely in two months. I feel like myself again.' },
    { name: 'Stephen Kariuki', town: 'Ol Kalou', county: 'Nyandarua', product: 'Tirzzy 5 mg', rating: 5, date: 'Aug 2026', text: 'My blood pressure readings at the clinic have improved alongside my diet changes, and I generally feel stronger. A good wellness companion.' },
    { name: 'Irene Wairimu', town: 'Nanyuki', county: 'Laikipia', product: 'Tirzzy 30 mg', rating: 5, date: 'Sep 2026', text: 'Tirzzy 30 mg is the real deal for stubborn fat. My waistline dropped two inches in six weeks. The gold packaging looks premium in my bathroom cabinet!' },
    { name: 'Collins Wafula', town: 'Kakamega', county: 'Kakamega', product: 'Tirzzy 15 mg', rating: 5, date: 'May 2026', text: 'Ordered on Monday, received on Wednesday. Tirzzy 15 mg helped me stop the 10pm ugali cravings. Down one belt notch already.' },
    { name: 'Nancy Kerubo', town: 'Nyamira', county: 'Nyamira', product: 'MOTS-C 10 mg', rating: 4, date: 'Jul 2026', text: 'Good steady energy for my market days which start very early. I only wish the bottle was bigger — I finished it in three weeks.' },
    { name: 'Anthony Mbugua', town: 'Embu', county: 'Embu', product: 'Tirzzy 5 mg', rating: 5, date: 'Aug 2026', text: 'I sleep deeper and wake up fresher since starting Tirzzy 5 mg. Even my joint stiffness in the morning has eased. Very happy customer.' },
    { name: 'Lilian Aoko', town: 'Kondele', county: 'Kisumu', product: 'Tirzzy 10 mg', rating: 5, date: 'Oct 2026', text: 'Second bottle now. First month I lost 4kg without starving myself. The team checks on your progress which keeps you motivated.' },
    { name: 'Victor Kipkorir', town: 'Bomet', county: 'Bomet', product: 'Tirzzy 15 mg', rating: 5, date: 'Jun 2026', text: 'As a boda rider I used to eat heavy meals twice a day. Now one balanced meal keeps me satisfied. My stomach is noticeably smaller.' },
    { name: 'Margaret Syombua', town: 'Kitui', county: 'Kitui', product: 'MOTS-C 10 mg', rating: 5, date: 'Sep 2026', text: 'Teaching lower primary needs endless energy! MOTS-C carries me through the day and evening prep. Delivery to Kitui was smooth.' },
    { name: 'Francis Maina', town: 'Meru', county: 'Meru', product: 'Tirzzy 30 mg', rating: 5, date: 'Jul 2026', text: 'At 45 I thought my big stomach was permanent. Tirzzy 30 mg proved me wrong — my old suits fit again. My wife has started on Tirzzy 15 mg.' },
    { name: 'Joyce Nyambura', town: 'Chuka', county: 'Tharaka-Nithi', product: 'Tirzzy 5 mg', rating: 5, date: 'Aug 2026', text: 'Gentle and natural feeling. My digestion, skin and mood all improved. I love that they give free guidance on WhatsApp before you buy.' },
    { name: 'Dennis Kiptoo', town: 'Iten', county: 'Elgeyo-Marakwet', product: 'Tirzzy 10 mg', rating: 4, date: 'May 2026', text: 'As a runner I wanted lean support without stimulants. Tirzzy 10 mg works well with training. Four stars because I want a bigger size for athletes.' },
    { name: 'Pauline Naliaka', town: 'Mbale', county: 'Vihiga', product: 'Tirzzy 15 mg', rating: 5, date: 'Sep 2026', text: 'Sweet cravings controlled from the first week. I have struggled with my weight for years and this is the first thing that feels sustainable.' },
    { name: 'Diba Wario', town: 'Marsabit', county: 'Marsabit', product: 'MOTS-C 10 mg', rating: 5, date: 'Jul 2026', text: 'I did not expect delivery to reach Marsabit so fast, but it arrived in three days well sealed. Energy+ helps me through long days at the shop.' },
    { name: 'Alice Waithera', town: 'Kitengela', county: 'Kajiado', product: 'Tirzzy 60 mg', rating: 5, date: 'Oct 2026', text: 'Bought the 60 mg course as a gift to myself for my birthday. The unboxing felt like Christmas! One month in: less snacking, more energy, 3kg down.' },
    { name: 'Joseph Lagat', town: 'Kitale', county: 'Trans Nzoia', product: 'Tirzzy 10 mg', rating: 5, date: 'Aug 2026', text: 'Quality product with proper branding and seals — no worries about fakes. 7kg down in two months with evening runs. Kitale delivery was fast.' },
    { name: 'Emily Chepkoech', town: 'Kabarnet', county: 'Baringo', product: 'Tirzzy 5 mg', rating: 5, date: 'Jun 2026', text: 'Tirzzy 5 mg helped my constant fatigue. I can now do my farm work and still have energy for the family in the evening. Asante Premium Supplements!' },
    { name: 'Patrick Mutua', town: 'Kilimani', county: 'Nairobi', product: 'Tirzzy 15 mg', rating: 5, date: 'Sep 2026', text: 'Working from home made me snack all day. Tirzzy 15 mg ended that habit in two weeks. Same-day delivery to Kilimani too. Impressive service.' },
    { name: 'Christine Adhiambo', town: 'Rongo', county: 'Migori', product: 'Tirzzy 30 mg', rating: 5, date: 'Jul 2026', text: 'My tummy after three kids is finally going down. Tirzzy 30 mg plus consistency works. The usage guide inside the box is very clear and simple.' },
    { name: 'Tom Onyango', town: 'Ugunja', county: 'Siaya', product: 'MOTS-C 10 mg', rating: 5, date: 'Aug 2026', text: 'I am a teacher and football coach — MOTS-C keeps me active on the pitch with the boys. No crash afterwards like energy drinks.' },
    { name: 'Sarah Wanjiru', town: 'Naivasha', county: 'Nakuru', product: 'Tirzzy 5 mg', rating: 4, date: 'May 2026', text: 'Nice gentle wellness formula. My sleep and digestion improved. Delivery took an extra day but support kept me updated on WhatsApp throughout.' },
    { name: 'Peter Odhiambo', town: 'Kilifi', county: 'Kilifi', product: 'Tirzzy 10 mg', rating: 5, date: 'Sep 2026', text: 'Down from 96kg to 88kg in two months with Tirzzy 10 mg and swimming. My tailor is tired of adjusting my clothes! Genuine product, highly recommended.' },
    { name: 'Agnes Mwikali', town: 'Diani', county: 'Kwale', product: 'Tirzzy 15 mg', rating: 5, date: 'Oct 2026', text: 'Hotel work means eating at odd hours. Tirzzy 15 mg helps me stay on top of portions no matter the shift. Delivery to Diani was quick.' },
    { name: 'John Kagia', town: 'Voi', county: 'Taita-Taveta', product: 'MOTS-C 10 mg', rating: 5, date: 'Jul 2026', text: 'Long truck routes between Voi and Nairobi need real stamina. MOTS-C is now part of my daily routine. No side effects for me.' },
    { name: 'Esther Nyakio', town: 'Narok', county: 'Narok', product: 'Tirzzy 5 mg', rating: 5, date: 'Aug 2026', text: 'My whole house uses Tirzzy 5 mg now — me, my mum and my sister. We all feel more active and our skin is glowing. Great family wellness product.' },
    { name: 'Moses Wanjala', town: 'Kapenguria', county: 'West Pokot', product: 'Tirzzy 10 mg', rating: 5, date: 'Jun 2026', text: 'I ordered with some fear because of online scams, but the parcel arrived sealed with proper branding. 5kg down and feeling confident.' },
    { name: 'Rose Atieno', town: 'Lodwar', county: 'Turkana', product: 'Tirzzy 15 mg', rating: 4, date: 'Jul 2026', text: 'Delivery to Lodwar took four days but it arrived safely. Tirzzy 15 mg is helping me eat smaller meals. Support team was honest about timelines.' },
    { name: 'Bernard Rotich', town: 'Maralal', county: 'Samburu', product: 'MOTS-C 10 mg', rating: 5, date: 'Sep 2026', text: 'Safari guiding needs early mornings and long days. MOTS-C keeps me sharp for my guests from dawn to sunset. Excellent product.' },
    { name: 'Clara Mideva', town: 'Isiolo', county: 'Isiolo', product: 'Tirzzy 5 mg', rating: 5, date: 'Aug 2026', text: 'Tirzzy 5 mg calmed my bloating and I feel lighter every day. The free consultation helped me pick the right product. Very professional team.' },
    { name: 'Yusuf Abdalla', town: 'Garissa', county: 'Garissa', product: 'Tirzzy 10 mg', rating: 5, date: 'May 2026', text: 'Down 8kg in two months with Tirzzy 10 mg and walking. My diabetes nurse is pleased with my progress. Delivery to Garissa was well packed and fast.' },
    { name: 'Halima Mohamed', town: 'Wajir', county: 'Wajir', product: 'Tirzzy 15 mg', rating: 5, date: 'Jul 2026', text: 'Tirzzy 15 mg helped me change my eating habits without feeling hungry all the time. The team explained usage clearly on WhatsApp. Shukran!' },
    { name: 'Abdi Ibrahim', town: 'Mandera', county: 'Mandera', product: 'MOTS-C 10 mg', rating: 5, date: 'Sep 2026', text: 'Shopkeeping from 6am to 10pm is exhausting. MOTS-C gives me clean steady strength through the day. Reached Mandera safely in four days.' },
    { name: 'Beatrice Auma', town: 'Lamu Island', county: 'Lamu', product: 'Tirzzy 60 mg', rating: 5, date: 'Aug 2026', text: 'Even here on the island, my 60 mg course arrived beautifully packed. It feels like a full wellness programme in a box. My energy and shape are transforming.' },
    { name: 'Nicholus Muema', town: 'Hola', county: 'Tana River', product: 'Tirzzy 30 mg', rating: 5, date: 'Oct 2026', text: 'Tirzzy 30 mg is strong and effective — my belly fat is melting with consistent use and morning walks. Proud to support a Kenyan wellness brand!' }
  ];

  const REVIEWS_PER_PAGE = 9;

  const makeWhatsAppUrl = (message) =>
    `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;

  const productGrid = document.getElementById('productGrid');
  const chipContainer = document.getElementById('chips');
  const searchInput = document.getElementById('searchInput');
  const emptyState = document.getElementById('emptyState');
  let activeCategory = 'All';

  function createProductCard(product, index) {
    const card = document.createElement('article');
    card.className = 'product-card product-shop-card';

    const media = document.createElement('div');
    media.className = 'product-media';

    const img = document.createElement('img');
    img.src = product.image;
    img.alt = `Sealed ${product.name} vial — ${product.category} by Premium Supplements`;
    img.loading = 'lazy';
    media.append(img);

    const badge = document.createElement('span');
    badge.className = 'product-badge';
    badge.textContent = product.badge;
    media.append(badge);

    const number = document.createElement('span');
    number.className = 'product-number product-media-number';
    number.textContent = String(index + 1).padStart(2, '0');
    media.append(number);

    const body = document.createElement('div');
    body.className = 'product-body';

    const category = document.createElement('span');
    category.className = 'product-category';
    category.textContent = product.category;

    const title = document.createElement('h3');
    title.textContent = product.name;

    const description = document.createElement('p');
    description.textContent = product.description;

    const priceRow = document.createElement('div');
    priceRow.className = 'product-price-row';

    const price = document.createElement('strong');
    price.className = 'product-price';
    price.textContent = formatKSh(product.price);

    const priceNote = document.createElement('span');
    priceNote.className = 'product-price-note';
    priceNote.textContent = 'Confirm via WhatsApp';
    priceRow.append(price, priceNote);

    const link = document.createElement('a');
    link.className = 'product-order';
    link.href = makeWhatsAppUrl(
      `Hello Premium Supplements, I would like to order ${product.name} (${product.category}) — ${formatKSh(product.price)}. Please confirm availability and delivery.`
    );
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.append(document.createTextNode('Order on WhatsApp '));

    const arrow = document.createElement('span');
    arrow.setAttribute('aria-hidden', 'true');
    arrow.textContent = '↗';
    link.append(arrow);

    body.append(category, title, description, priceRow, link);
    card.append(media, body);
    return card;
  }

  function renderProducts() {
    if (!productGrid) return;

    const query = searchInput?.value.trim().toLocaleLowerCase() || '';
    const visibleProducts = products.filter((product) => {
      const matchesCategory = activeCategory === 'All' || product.category === activeCategory;
      const searchableText = `${product.name} ${product.category} ${product.description} ${product.price}`.toLocaleLowerCase();
      return matchesCategory && searchableText.includes(query);
    });

    const cards = visibleProducts.map((product) => createProductCard(product, products.indexOf(product)));
    productGrid.replaceChildren(...cards);
    if (emptyState) emptyState.hidden = cards.length > 0;
  }

  function setActiveCategory(label, options = {}) {
    activeCategory = label;
    if (chipContainer) {
      chipContainer.querySelectorAll('.chip').forEach((chip) => {
        const isActive = chip.dataset.category === label;
        chip.classList.toggle('is-active', isActive);
        chip.setAttribute('aria-pressed', String(isActive));
      });
    }
    renderProducts();
    if (options.scroll) {
      document.getElementById('products')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  function createCategoryFilters() {
    if (!chipContainer) return;

    const labels = ['All', ...new Set(products.map((product) => product.category))];
    const fragment = document.createDocumentFragment();

    labels.forEach((label) => {
      const button = document.createElement('button');
      button.className = `chip${label === activeCategory ? ' is-active' : ''}`;
      button.type = 'button';
      button.dataset.category = label;
      button.textContent = label === 'All' ? 'All products' : label;
      button.setAttribute('aria-pressed', String(label === activeCategory));
      button.addEventListener('click', () => setActiveCategory(label));
      fragment.append(button);
    });

    chipContainer.replaceChildren(fragment);
  }

  function setupGoalCards() {
    document.querySelectorAll('.goal-card[data-category]').forEach((card) => {
      card.addEventListener('click', () => {
        setActiveCategory(card.dataset.category, { scroll: true });
      });
    });
  }

  /* ---------- Reviews ---------- */

  const reviewsGrid = document.getElementById('reviewsGrid');
  const reviewsSummary = document.getElementById('reviewsSummary');
  const reviewSearchInput = document.getElementById('reviewSearchInput');
  const reviewProductFilter = document.getElementById('reviewProductFilter');
  const reviewsEmpty = document.getElementById('reviewsEmpty');
  const reviewsMoreBtn = document.getElementById('reviewsMoreBtn');
  const reviewsCount = document.getElementById('reviewsCount');
  let reviewProduct = 'All';
  let reviewsShown = REVIEWS_PER_PAGE;

  const starString = (rating) => '★'.repeat(rating) + '☆'.repeat(5 - rating);

  const initialsOf = (name) =>
    name
      .split(' ')
      .map((part) => part.charAt(0))
      .slice(0, 2)
      .join('')
      .toUpperCase();

  function filteredReviews() {
    const query = reviewSearchInput?.value.trim().toLocaleLowerCase() || '';
    return reviews.filter((review) => {
      const matchesProduct = reviewProduct === 'All' || review.product === reviewProduct;
      const searchableText = `${review.name} ${review.town} ${review.county} ${review.product} ${review.text}`.toLocaleLowerCase();
      return matchesProduct && searchableText.includes(query);
    });
  }

  function createReviewCard(review) {
    const card = document.createElement('article');
    card.className = 'review-card';

    const head = document.createElement('div');
    head.className = 'review-head';

    const avatar = document.createElement('span');
    avatar.className = 'review-avatar';
    avatar.setAttribute('aria-hidden', 'true');
    avatar.textContent = initialsOf(review.name);

    const who = document.createElement('span');
    who.className = 'review-who';

    const name = document.createElement('strong');
    name.textContent = review.name;

    const place = document.createElement('small');
    place.textContent = `${review.town}, ${review.county}`;

    who.append(name, place);
    head.append(avatar, who);

    const stars = document.createElement('div');
    stars.className = 'review-stars';
    stars.setAttribute('aria-label', `Rated ${review.rating} out of 5`);
    stars.textContent = starString(review.rating);

    const text = document.createElement('p');
    text.className = 'review-text';
    text.textContent = `“${review.text}”`;

    const foot = document.createElement('div');
    foot.className = 'review-foot';

    const productTag = document.createElement('span');
    productTag.className = 'review-product';
    productTag.textContent = review.product;

    const meta = document.createElement('span');
    meta.className = 'review-meta';
    meta.textContent = `${review.date} · ✓ Verified buyer`;

    foot.append(productTag, meta);
    card.append(head, stars, text, foot);
    return card;
  }

  function renderReviews() {
    if (!reviewsGrid) return;

    const matches = filteredReviews();
    const visible = matches.slice(0, reviewsShown);
    reviewsGrid.replaceChildren(...visible.map(createReviewCard));

    if (reviewsEmpty) reviewsEmpty.hidden = matches.length > 0;
    if (reviewsCount) {
      reviewsCount.textContent = matches.length
        ? `Showing ${visible.length} of ${matches.length} review${matches.length === 1 ? '' : 's'}`
        : '';
    }
    if (reviewsMoreBtn) {
      reviewsMoreBtn.hidden = visible.length >= matches.length;
    }
  }

  function renderReviewsSummary() {
    if (!reviewsSummary) return;

    const total = reviews.length;
    const average = reviews.reduce((sum, review) => sum + review.rating, 0) / total;
    const fiveStar = reviews.filter((review) => review.rating === 5).length;
    const countyCount = new Set(reviews.map((review) => review.county)).size;
    const fiveStarPct = Math.round((fiveStar / total) * 100);

    reviewsSummary.innerHTML = '';

    const score = document.createElement('div');
    score.className = 'summary-score';

    const averageEl = document.createElement('strong');
    averageEl.textContent = average.toFixed(1);

    const stars = document.createElement('div');
    stars.className = 'stars';
    stars.setAttribute('aria-label', `Average rating ${average.toFixed(1)} out of 5`);
    stars.textContent = '★★★★★';

    const basedOn = document.createElement('span');
    basedOn.textContent = `Based on ${total} verified reviews`;

    score.append(averageEl, stars, basedOn);

    const stats = document.createElement('div');
    stats.className = 'summary-stats';

    const statData = [
      { value: String(countyCount), label: 'Counties represented' },
      { value: `${fiveStarPct}%`, label: 'Five-star reviews' },
      { value: String(new Set(reviews.map((review) => review.product)).size), label: 'Products reviewed' }
    ];

    statData.forEach((stat) => {
      const item = document.createElement('div');
      item.className = 'summary-stat';
      const value = document.createElement('strong');
      value.textContent = stat.value;
      const label = document.createElement('span');
      label.textContent = stat.label;
      item.append(value, label);
      stats.append(item);
    });

    reviewsSummary.append(score, stats);
  }

  function populateReviewFilter() {
    if (!reviewProductFilter) return;
    const fragment = document.createDocumentFragment();
    const reviewedProductNames = [...new Set(reviews.map((review) => review.product))].sort((a, b) =>
      a.localeCompare(b)
    );
    reviewedProductNames.forEach((name) => {
      const option = document.createElement('option');
      option.value = name;
      option.textContent = name;
      fragment.append(option);
    });
    reviewProductFilter.append(fragment);
  }

  function setupReviews() {
    if (!reviewsGrid) return;
    renderReviewsSummary();
    populateReviewFilter();
    renderReviews();

    if (reviewSearchInput) {
      reviewSearchInput.addEventListener('input', () => {
        reviewsShown = REVIEWS_PER_PAGE;
        renderReviews();
      });
    }
    if (reviewProductFilter) {
      reviewProductFilter.addEventListener('change', () => {
        reviewProduct = reviewProductFilter.value;
        reviewsShown = REVIEWS_PER_PAGE;
        renderReviews();
      });
    }
    if (reviewsMoreBtn) {
      reviewsMoreBtn.addEventListener('click', () => {
        reviewsShown += REVIEWS_PER_PAGE;
        renderReviews();
      });
    }
  }

  /* ---------- Forms & navigation ---------- */

  function populateFormSelects() {
    const countySelect = document.getElementById('fCounty');
    const productSelect = document.getElementById('fProduct');

    if (countySelect) {
      const fragment = document.createDocumentFragment();
      counties.forEach((county) => {
        const option = document.createElement('option');
        option.value = county;
        option.textContent = county;
        fragment.append(option);
      });
      countySelect.append(fragment);
    }

    if (productSelect) {
      const fragment = document.createDocumentFragment();
      products.forEach((product) => {
        const option = document.createElement('option');
        option.value = product.name;
        option.textContent = `${product.name} — ${formatKSh(product.price)}`;
        fragment.append(option);
      });
      productSelect.append(fragment);
    }
  }

  function setupContactForm() {
    const form = document.getElementById('contactForm');
    const error = document.getElementById('formError');
    if (!form) return;

    form.addEventListener('submit', (event) => {
      event.preventDefault();

      const formData = new FormData(form);
      const name = String(formData.get('name') || '').trim();
      const phone = String(formData.get('phone') || '').trim();
      const county = String(formData.get('county') || '').trim();
      const product = String(formData.get('product') || '').trim();
      const message = String(formData.get('message') || '').trim();

      if (!name || !phone) {
        if (error) error.hidden = false;
        return;
      }

      if (error) error.hidden = true;
      const lines = [
        'Hello Premium Supplements,',
        '',
        `My name is ${name}.`,
        `My phone number is ${phone}.`,
        county ? `County: ${county}.` : '',
        product ? `Product interest: ${product}.` : '',
        message ? `Message: ${message}` : ''
      ].filter(Boolean);

      window.open(makeWhatsAppUrl(lines.join('\n')), '_blank', 'noopener,noreferrer');
    });

    form.addEventListener('input', () => {
      if (error) error.hidden = true;
    });
  }

  function setupNavigation() {
    const menuButton = document.getElementById('menuBtn');
    const navLinks = document.getElementById('navLinks');
    if (!menuButton || !navLinks) return;

    const closeMenu = () => {
      menuButton.setAttribute('aria-expanded', 'false');
      navLinks.classList.remove('is-open');
    };

    menuButton.addEventListener('click', () => {
      const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
      menuButton.setAttribute('aria-expanded', String(!isOpen));
      navLinks.classList.toggle('is-open', !isOpen);
    });

    navLinks.querySelectorAll('a[href^="#"]').forEach((link) => {
      link.addEventListener('click', () => {
        closeMenu();
        navLinks.querySelectorAll('a').forEach((item) => item.classList.remove('is-active'));
        link.classList.add('is-active');
      });
    });

    document.addEventListener('click', (event) => {
      if (!navLinks.contains(event.target) && !menuButton.contains(event.target)) closeMenu();
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') closeMenu();
    });

    if ('IntersectionObserver' in window) {
      const sections = document.querySelectorAll('main [data-section]');
      const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const activeLink = navLinks.querySelector(`a[href="#${entry.target.id}"]`);
          if (!activeLink) return;
          navLinks.querySelectorAll('a').forEach((link) => link.classList.remove('is-active'));
          activeLink.classList.add('is-active');
        });
      }, { rootMargin: '-35% 0px -55% 0px' });
      sections.forEach((section) => observer.observe(section));
    }
  }

  /* Headline words that keep refreshing: the swap span flips out, swaps its
     word and flips back in (see .swap-word in css/style.css). */
  function setupWordSwaps() {
    const swappers = document.querySelectorAll('.swap-word');
    if (!swappers.length) return;
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    swappers.forEach((el, index) => {
      const words = (el.dataset.words || '').split('|').map((w) => w.trim()).filter(Boolean);
      if (reduceMotion || words.length < 2) return;
      let i = 0;
      window.setInterval(() => {
        el.classList.add('is-out');
        window.setTimeout(() => {
          i = (i + 1) % words.length;
          el.textContent = words[i];
          el.classList.add('is-in');
          el.classList.remove('is-out');
          requestAnimationFrame(() => requestAnimationFrame(() => el.classList.remove('is-in')));
        }, 430);
      }, 3200 + index * 700);
    });
  }

  const year = document.getElementById('year');
  if (year) year.textContent = String(new Date().getFullYear());

  createCategoryFilters();
  populateFormSelects();
  renderProducts();
  if (searchInput) searchInput.addEventListener('input', renderProducts);
  setupGoalCards();
  setupReviews();
  setupContactForm();
  setupNavigation();
  setupWordSwaps();
})();
