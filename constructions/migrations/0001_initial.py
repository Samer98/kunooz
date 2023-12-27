# Generated by Django 4.2.6 on 2023-12-27 21:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('project_number', models.PositiveIntegerField()),
                ('style', models.CharField(max_length=255)),
                ('room_number', models.IntegerField(default=0)),
                ('space', models.IntegerField(default=0)),
                ('location', models.CharField(choices=[('Cairo', 'Cairo'), ('Alexandria', 'Alexandria'), ('Giza', 'Giza'), ('Luxor', 'Luxor'), ('Aswan', 'Aswan'), ('Sharm El Sheikh', 'Sharm El Sheikh'), ('Hurghada', 'Hurghada'), ('Port Said', 'Port Said'), ('Damietta', 'Damietta'), ('Mansoura', 'Mansoura'), ('Sohag', 'Sohag'), ('Ismailia', 'Ismailia'), ('Minya', 'Minya'), ('Assiut', 'Assiut'), ('Tanta', 'Tanta'), ('Beni Suef', 'Beni Suef'), ('Faiyum', 'Faiyum'), ('Zagazig', 'Zagazig'), ('Suez', 'Suez'), ('Qena', 'Qena'), ('Damanhur', 'Damanhur'), ('El Mahalla El Kubra', 'El Mahalla El Kubra'), ('Kafr El Sheikh', 'Kafr El Sheikh'), ('Mallawi', 'Mallawi'), ('El Arish', 'El Arish'), ('Kafr El Minya', 'Kafr El Minya'), ('Banha', 'Banha'), ('Kafr El Dawwar', 'Kafr El Dawwar'), ('Qalyub', 'Qalyub'), ('Desouk', 'Desouk'), ('Abu Kabir', 'Abu Kabir'), ('Mataria', 'Mataria'), ('Egypt Suez', 'Egypt Suez'), ('Port Fouad', 'Port Fouad'), ('Port Said', 'Port Said'), ('Al Fashn', 'Al Fashn'), ('Fuwa', 'Fuwa'), ('Matrouh', 'Matrouh'), ('Gamasa', 'Gamasa'), ('Bilbeis', 'Bilbeis'), ('Shubra El Kheima', 'Shubra El Kheima'), ('Kom Ombo', 'Kom Ombo'), ('Qus', 'Qus'), ('Abu Tisht', 'Abu Tisht'), ('Armant', 'Armant'), ('Akhmim', 'Akhmim'), ('Az Zaqaziq', 'Az Zaqaziq'), ('Ibb', 'Ibb'), ('Kom Hamada', 'Kom Hamada'), ('El Balyana', 'El Balyana'), ('Basyoun', 'Basyoun'), ('Manfalut', 'Manfalut'), ('Tala', 'Tala'), ('Kawm Umbu', 'Kawm Umbu'), ('Tama', 'Tama'), ('Fua', 'Fua'), ('Mashtul El Souq', 'Mashtul El Souq'), ('Tahta', 'Tahta'), ('Amin', 'Amin'), ('Quwaysina', 'Quwaysina'), ('Aswan Governorate', 'Aswan Governorate'), ('Kom Ghaybah', 'Kom Ghaybah'), ('Samalut', 'Samalut'), ('Ushmun', 'Ushmun'), ('Girga', 'Girga'), ('Dayrut', 'Dayrut'), ('Tukh', 'Tukh'), ('Tahta', 'Tahta'), ('Naj 3hammadi', 'Naj 3hammadi'), ('Abu Al Matamir', 'Abu Al Matamir'), ('Hawsh Eissa', 'Hawsh Eissa'), ('El Tor', 'El Tor'), ('Huwaydiyat', 'Huwaydiyat'), ('Bani Suwef', 'Bani Suwef'), ('Kawm Hamadah', 'Kawm Hamadah'), ('Fuwwah', 'Fuwwah'), ('Kom Ash Shuqqafa', 'Kom Ash Shuqqafa'), ('Desuq', 'Desuq'), ('Zifta', 'Zifta'), ('Rashid', 'Rashid'), ('Minyat an Nasr', 'Minyat an Nasr'), ('Bibas', 'Bibas'), ('Baltim', 'Baltim'), ('Raml Station', 'Raml Station'), ('Faiyum', 'Faiyum'), ('El Faiyum', 'El Faiyum'), ('Jirja', 'Jirja'), ('Mallawi', 'Mallawi'), ('Matay', 'Matay'), ('Al Bajur', 'Al Bajur'), ('Bani Mazar', 'Bani Mazar'), ('Santa', 'Santa'), ('Faqus', 'Faqus'), ('El Ibrahimiyah', 'El Ibrahimiyah'), ('Ibsheway', 'Ibsheway'), ('Dayrut', 'Dayrut'), ('Tala', 'Tala'), ('El Kawm Ash Sharqiyah', 'El Kawm Ash Sharqiyah'), ('Ashmun', 'Ashmun'), ('Almansha', 'Almansha'), ('Ad-Dakahlia', 'Ad-Dakahlia'), ('El Mahalla El Kubra', 'El Mahalla El Kubra'), ('Kafr El Zayat', 'Kafr El Zayat'), ('Sanabu', 'Sanabu'), ('Karasine', 'Karasine'), ('Bishnupur', 'Bishnupur'), ('Sidi Salem', 'Sidi Salem'), ('Al Hamdaniya', 'Al Hamdaniya'), ('Banha', 'Banha'), ('Komsomolsk', 'Komsomolsk'), ('Sidi Salem', 'Sidi Salem'), ('Santa', 'Santa'), ('Dahab', 'Dahab'), ('Alkom Ash Shuwayfat', 'Alkom Ash Shuwayfat'), ('Naqadah', 'Naqadah'), ('Etay Al Barud', 'Etay Al Barud'), ('Fuqaha', 'Fuqaha'), ('Bulaq', 'Bulaq'), ('Shaykh Zuwayd', 'Shaykh Zuwayd'), ('Madinat Sittah Uktubar', 'Madinat Sittah Uktubar'), ('Dairut', 'Dairut')], default='Cairo', max_length=255)),
                ('outer_design', models.CharField(choices=[('ٌResidential', 'Residential'), ('Commercial', 'Commercial'), ('industrial', 'industrial'), ('General', 'General'), ('Farms', 'Farms')], default='ٌResidential', max_length=255)),
                ('total_budget', models.PositiveIntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(choices=[('On Going', 'On Going'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], default='On Going', max_length=255)),
                ('project_owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project_members',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='constructions.project')),
            ],
        ),
    ]
