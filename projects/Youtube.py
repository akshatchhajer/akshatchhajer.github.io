#!/usr/bin/env python
# coding: utf-8

# In[40]:


from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns


# In[74]:


api_key = 'AIzaSyAn3du_COtTPFbc0PSMXDHJzXxmVCWtOQY'
channel_ids = ['UCLLw7jmFsvfIVaUFsLs8mlQ', # Luke Barousse 
               'UCiT9RITQ9PW6BhXK0y2jaeg', # Ken Jee
               'UC7cs8q-gJRlGwj4A8OmCmXg', # Alex the analyst
               'UC2UXDak6o7rBm23k3Vv5dww', # Tina Huang
               'UC3rY5HOgbBvGmq7RnDfwF7A' #Rishabh Mishra
              ]

youtube = build('youtube', 'v3', developerKey=api_key)


# In[75]:


def get_channel_stats(youtube, channel_ids):
    all_data = []
    request = youtube.channels().list(
                part='snippet,contentDetails,statistics',
                id=','.join(channel_ids))
    response = request.execute() 
    
    for i in range(len(response['items'])):
        data = dict(Channel_name = response['items'][i]['snippet']['title'],
                    Subscribers = response['items'][i]['statistics']['subscriberCount'],
                    Views = response['items'][i]['statistics']['viewCount'],
                    Total_videos = response['items'][i]['statistics']['videoCount'],
                    playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        all_data.append(data)
    
    return all_data


# In[76]:


channel_statistics = get_channel_stats(youtube, channel_ids)


# In[77]:


channel_data = pd.DataFrame(channel_statistics)


# In[78]:


channel_data['Subscribers'] = pd.to_numeric(channel_data['Subscribers'])
channel_data['Views'] = pd.to_numeric(channel_data['Views'])
channel_data['Total_videos'] = pd.to_numeric(channel_data['Total_videos'])


# In[114]:


playlist_id = channel_data.loc[channel_data['Channel_name']=='Rishabh Mishra', 'playlist_id'].iloc[0]


# In[115]:


playlist_id


# In[116]:


def get_video_ids(youtube, playlist_id):
    
    request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId = playlist_id,
                maxResults = 50)
    response = request.execute()
    
    video_ids = []
    
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])
        
    next_page_token = response.get('nextPageToken')
    more_pages = True
    
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                        part='contentDetails',
                        playlistId = playlist_id,
                        maxResults = 50,
                        pageToken = next_page_token)
            response = request.execute()
    
            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])
            
            next_page_token = response.get('nextPageToken')
        
    return video_ids


# In[117]:


video_ids = get_video_ids(youtube, playlist_id)


# In[118]:


def get_video_details(youtube, video_ids):
    all_video_stats = []
    
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
                    part='snippet,statistics',
                    id=','.join(video_ids[i:i+50]))
        response = request.execute()
        
        for video in response['items']:
            video_stats = dict(Title = video['snippet']['title'],
                               Published_date = video['snippet']['publishedAt'],
                               Views = video['statistics']['viewCount'],
                               Likes = video['statistics']['likeCount'],
                               Comments = video['statistics']['commentCount']
                               )
            all_video_stats.append(video_stats)
    
    return all_video_stats


# In[119]:


video_details = get_video_details(youtube, video_ids)


# In[120]:


video_data = pd.DataFrame(video_details)


# In[121]:


video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date
video_data['Views'] = pd.to_numeric(video_data['Views'])
video_data['Likes'] = pd.to_numeric(video_data['Likes'])
video_data['Views'] = pd.to_numeric(video_data['Views'])


# In[122]:


plt.figure(figsize=(9,4))
sns.barplot(data=channel_data,x="Channel_name",y="Subscribers")


# In[123]:


plt.figure(figsize=(9,4))
sns.barplot(data=channel_data,x="Channel_name",y="Views")


# In[129]:


plt.figure(figsize=(9,4))
channel_data["Views_per_subs"]=channel_data["Views"]/channel_data["Subscribers"]
channel_data["Views_per_subs"]=channel_data["Views_per_subs"].round(0)

sns.scatterplot(data=channel_data,x="Channel_name",y="Views_per_subs")


# In[131]:


plt.style.use("ggplot")
fig, axs = plt.subplots(1,2, figsize=(15,9), sharex=True)
sns.barplot(data=channel_data,x="Channel_name",y="Total_videos",ax=axs[0])


plt.subplot(1,2,2)
plt.figure(figsize=(9,4))
channel_data["Views_per_vids"]=channel_data["Views"]/channel_data["Total_videos"]
channel_data["Views_per_vids"]=channel_data["Views_per_vids"].round(0)

sns.barplot(data=channel_data,x="Channel_name",y="Views_per_vids",ax=axs[1])

plt.tight_layout()


# In[127]:


top10_videos = video_data.sort_values(by='Views', ascending=False).head(10)


# In[128]:


ax1 = sns.barplot(x='Views', y='Title', data=top10_videos)


# In[126]:


video_data["Month"]=pd.to_datetime(video_data['Published_date']).dt.strftime('%b')
sns.countplot(data=video_data,x="Month")


# In[ ]:





# In[ ]:




