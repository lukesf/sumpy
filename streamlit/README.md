#  Streamlit on Raspi 
![Streamlit Dashboard](streamlit-dashboard.jpg)

Streamlit is awesome way to get userspace httpd dashboard  
Want to use pandas so some dependencies :-/ 

## Troublesome apache arrow dependency
```
sudo apt-get install python-dev libatlas-base-dev
sudo pip3 install numpy pandas plotly
```
### Issue: Streamlit depends on pyarrow which nolonger supports 32bit OSs :-(
* ~~Deadend with apache arrow dependency~~
* https://discuss.streamlit.io/t/how-to-install-streamlit-on-32-bit-pc/5529
* https://discuss.streamlit.io/t/raspberry-pi-streamlit/2900/26?page=2
**Solution: For 32bit OSes Don't need latest and greatest so alternative happy path. Use older Streamlit before pyarrow dependency was added:**
```
sudo pip3 install streamlit==0.62.0
```
* There also seems to be a bug with dataframes and line_chart so reverted to pyplot
**For 64bit OSes can just use latest:**
```
sudo pip3 install streamlit
```

## To execute:
````
streamlit run sump_streamlit.py
```
Notes:
* water and temp in the raspi csv directory
* point browser at [http://localhost:8501](http://localhost:8501)
* make init scripts so starts as service on boot



## References
* https://streamlit.io/
